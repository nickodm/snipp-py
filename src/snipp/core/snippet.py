from __future__ import annotations

from pathlib import Path, PurePath
from pathvalidate import sanitize_filename
from uuid import uuid4
from datetime import datetime
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, IO

if TYPE_CHECKING:
    from typing_extensions import Self

import tomlkit as t
import logging as _logging
import fastjsonschema
import struct
import py7zr
import json
import os
import io

from .. import schemas
from .paths import SNIPPETS
from .errors import *

from snipp import __version_info__

logger = _logging.getLogger(__name__)

def compact_json(obj) -> bytes:
    def try_serialize(obj):
        if hasattr(obj, "as_json"):
            return obj.as_json().encode()
        else:
            raise TypeError
    
    return json.dumps(
        obj,
        separators=(',', ':'),
        default=try_serialize
    ).encode()


class Metadata:
    """
    A class representing the metadata of a snippet.
    """
    
    def __init__(self, name: str, description: str = "", git_init: bool = True):
        self.name: str = name
        self.id: str = str(uuid4())
        self.description: str = description
        self.git_init: bool = git_init
        self.creation_date: datetime | None = datetime.now()
        self.software_version: tuple = __version_info__
    
    @classmethod
    def _validate_schema(cls, d: dict) -> bool:
        """Validate the schema of the dictionary.

        :param dict d: The dictionary to validate.
        :return bool: Whether the schema is valid.
        """
        
        try:
            schemas.metadata.validate(d)
            return True
        except fastjsonschema.JsonSchemaException:
            logger.exception("Metadata JSON schema validation error")
            return False
    
    def sanitized_name(self) -> str:
        return sanitize_filename(self.name)
        
    def as_toml(self) -> str:
        """Render the metadata information as a TOML.

        :return str: The TOML as a string.
        """
        doc = t.document()
        
        info = t.table()
        info.add(t.comment("The name to display."))
        info.add("name", self.name)
        
        info.add(t.comment("DO NOT TOUCH!"))
        info.add("id", self.id)
        
        info.add(t.comment("The description of the snippet."))
        info.add("description", self.description)
        
        info.add(t.comment("Whether to init a git repository when "
                           "using the snippet."))
        info.add("git_init", self.git_init)
        
        if self.creation_date is not None:
            info.add(t.comment("The date when the snippet was created."))
            info.add("creation_date", self.creation_date)
        
        doc.add("snippet-info", info)
        
        software_info = t.table()
        
        software_info.add(t.comment("The version of snipp used to create this "
                                    "snippet."))
        software_info.add("version", __version_info__)
        
        doc.add("software-info", software_info)
        
        return doc.as_string()
    
    def as_json(self, *, indent: int | None = None,
                include_id: bool = False) -> str:
        """Dump the metadata as a JSON.
        
        :param int | None indent: The indentation for the JSON,
        defaults to None
        :param bool include_id: Whether to include the ID in the JSON.
        :return str: The metadata as a JSON.
        """
        data: dict[str, dict] = {
            "snippet-info": {
                "name": self.name,
                "id": self.id,
                "description": self.description,
                "git_init": self.git_init,
                "creation_date": self.creation_date.toordinal(),
            },
            "software-info": {
                "version": self.software_version
            }
        }
        
        if not include_id:
            data["snippet-info"].pop("id")
        
        separators: tuple[str] = (',', ':') if indent is None else (',', ': ')
        return json.dumps(data, indent=indent, separators=separators)
    
    @classmethod
    def from_dict(cls, d: dict) -> Self:
        """Load a snippet's metadata from a dictionary.

        :param dict d: The dictionary.
        :return Self: The loaded metadata.
        """
        self = cls.__new__(cls)
        
        info: dict = d.get("snippet-info", {})
        
        self.name = info.get("name", "[Unnamed]")
        self.id = info.get("id", str(uuid4()))
        self.description = info.get("description", "")
        self.git_init = info.get("git_init", True)
        self.creation_date = info.get("creation_date", None)
        
        software_info: dict = d.get("software-info", {})
        self.software_version = tuple(software_info.get("version", 
                                                        __version_info__))
        
        return self
    
    @classmethod
    def from_toml(cls, source: str | bytes) -> Self:
        """Parse the metadata information from a TOML string.

        :param str | bytes source: The TOML as a string or bytes.
        :return Self: The loaded metadata.
        """
        return cls.from_dict(t.parse(source))
    
    @classmethod
    def from_json(cls, source: str | bytes) -> Self:
        """Parse the metadata information from a JSON string.

        :param str | bytes source: The JSON as a string or bytes.
        :return Self: The loaded metadata.
        :raises InvalidMetadataError: When the loaded metadata is invalid.
        """
        data: dict = json.loads(source)
        
        if not cls._validate_schema(data):
            raise InvalidMetadataError()
        
        info = data["snippet-info"]
        info["creation_date"] = datetime.fromordinal(info["creation_date"])
        return cls.from_dict(data)
    
    @classmethod
    def extract(cls, file: SnippFile) -> Self:
        """Extract the metadata of a snippet from an opened SnippFile.

        :param ZipFile zf: The opened SnippFile.
        :return Self: The extracted metadata.
        """
        data = file.read_part("metadata")
        self = cls.from_json(data)
        self.id = file.id
        return self


class SnippFile:
    """
    Builder and parser class for .snipp files.
    """
    
    SUFFIX: str = ".snipp"
    """The suffix for the snipp files."""
    
    HEADER_FMT: str = ">5s36sQ"
    """The header's binary format."""

    HEADER_SIZE: int = struct.calcsize(HEADER_FMT)
    """The header's size."""
    
    # OBFUSCATE_KEY: int = 12
    # """The key to obsfuscate the bytes."""
    
    def __init__(self, file: Path | str | IO[bytes], mode: str = "r") -> None:
        """Read or write a snipp file into `file`.

        :param Path | str | IO[bytes] file: The destination of the snipp
        file.
        :param str mode: The mode to open the snipp file, defaults to "r"
        :raises InvalidSnippetError: When the snipp file is invalid.
        """
        self._metadata: Metadata | None = None
        self._file_index: list[str] = []
        self._contents: bytes | None = None
        self._index: dict[str, dict[str, int]] = {}
        self._id: str | None = None
        self._mode: str = mode
        
        if isinstance(file, (os.PathLike, str)):
            self.fp: IO[bytes] = open(file, mode + "b")
        else:
            self.fp: IO[bytes] = file
        
        if mode != "r":
            return

        # Read Header
        self.id, index_pos = self._read_header(self.fp)

        # Read index
        self.fp.seek(index_pos)
        index: bytes = self.fp.read()
        try:
            self._index = schemas.index.validate(json.loads(index))
        except (fastjsonschema.JsonSchemaException, json.JSONDecodeError):
            logger.exception("SnippFile invalid index: %r", index)
            raise InvalidSnippetError()
    
    @classmethod
    def _read_header(cls, fp: IO[bytes]) -> tuple[str, int]:
        """Read the header in `fp` and return it's information.

        :param IO[bytes] fp: The IO containing the snipp file.
        :raises InvalidSnippetError: When the snipp file is invalid.
        :return tuple[str, int]: The ID and the index_pos.
        """
        header = fp.read(cls.HEADER_SIZE)
        
        try:
            magic, id, index_pos = struct.unpack(cls.HEADER_FMT, header)
        except (struct.error, IOError):
            raise InvalidSnippetError()
        
        if magic != b"SNIPP":
            raise InvalidSnippetError()
        
        return id.decode(), index_pos

    @classmethod
    def check_id(cls, file: Path | str | IO[bytes], id_check: str) -> bool:
        """Check if the snipp file's ID is equal to `ìd_check`.

        :param Path | str | IO[bytes] file: The snipp file.
        :param str id_check: The ID to compare with the snipp file's ID.
        :return bool: Whether both IDs are equal.
        """
        if isinstance(file, (os.PathLike, str)):
            fp = open(file, "rb")
        else:
            fp = file

        try:
            with fp:
                id, _ = cls._read_header(fp)
        except InvalidSnippetError:
            return False

        return id == id_check

    @property
    def closed(self) -> bool:
        return self.fp.closed
    
    @property
    def id(self) -> str | None:
        return self._id
    
    def add_metadata(self, metadata: Metadata) -> Self:
        """Add the snippet's metadata to the file.

        :param Metadata metadata: The snippet's metadata.
        :return Self:
        """
        self._check_mode("w")
        self._metadata = metadata
        self._id = metadata.id
        return self
        
    def add_file_index(self, source: list[PurePath | str]) -> Self:
        """Add the file index of the snippet.

        :param list[PurePath | str] source: The list of files in the snippet.
        :return Self:
        """
        self._check_mode("w")
        for path in source:
            if isinstance(path, PurePath):
                path: str = path.as_posix()
            
            self._file_index.append(path)
        return self
    
    # def add_choices(self) -> Self: ...
    # def add_commands(self) -> Self: ...
    # def add_hooks(self) -> Self: ...

    def add_contents(self, contents: bytes) -> Self:
        """Add the contents of the snipp file as bytes. This is the
        compressed file, in 7z format.

        :param bytes contents: The contents of the snippet.
        :return Self:
        """
        self._check_mode("w")
        self._contents = contents
        return self
        
    def _generate_header(self, index_pos: int) -> bytes:
        """Generate the snippet file header."""
        self._check_mode("w")
        id: bytes = self._id.encode()
        return struct.pack(self.HEADER_FMT, b"SNIPP", id, index_pos)
    
    def _write_part(self, name: str, source: bytes) -> None:
        """Write the source bytes to the file and save the part in the
        index.

        :param str name: The name of the part to append and index.
        :param bytes source: The part to append in bytes.
        """
        self._check_mode("w")
        pos = self.fp.tell()
        size = self.fp.write(source)
        self._index[name] = {
            "pos": pos,
            "size": size
        }
    
    def build(self) -> None:
        """Build the snipp file with the added information."""
        self._check_mode("w")
        fp = self.fp
        fp.seek(self.HEADER_SIZE)
        
        metadata: bytes = self._metadata.as_json().encode()
        self._write_part("metadata", metadata)
        
        file_index: bytes = compact_json(self._file_index)
        self._write_part("file_index", file_index)
        
        self._write_part("contents", self._contents)
        
        index_pos: int = fp.tell()
        index: bytes = compact_json(self._index)
        fp.write(index)
        
        fp.seek(0)
        header: bytes = self._generate_header(index_pos)
        fp.write(header)
    
    def read_part(self, name: str) -> bytes | None:
        """Read a part of the snipp file.

        :param str name: The part's name.
        :return bytes | None: The bytes of the part, is exists.
        :raises ValueError: When the snipp file is closed.
        """
        if self.closed:
            raise ValueError("I/O operation on closed file.")
        
        part: dict[str, int] | None = self._index.get(name)
        
        if part is None:
            return None
        
        pos = part["pos"]
        size = part["size"]
        
        self.fp.seek(pos)
        return self.fp.read(size)
    
    def list_parts(self) -> list[str]:
        """List all the file's parts."""
        return [k for k in self._index.keys()]

    def close(self) -> None:
        """Close the snipp file."""
        self._metadata = None
        self._contents = None
        self._file_index.clear()
        self._index.clear()
        self.fp.close()
    
    # @classmethod
    # def _obfuscate(cls, data: bytes) -> bytes:
    #     return bytes([b ^ cls.OBFUSCATE_KEY for b in data])

    def __enter__(self) -> Self:
        return self
    
    def __exit__(self, exc_type, exc, tb):
        if self._mode == "w":
            self.build()
        
        self.close()
    
    def __repr__(self) -> str:
        return f"<SnippFile mode={self._mode}, id={self._id}>"

    def _check_mode(self, mode: str) -> None:
        if self._mode != mode:
            raise io.UnsupportedOperation


class Snippet:    
    ID_MIN_LEN: int = 7
    """The minimum length to use an ID."""
    
    SUFFIX: str = ".snipp"
    """The suffix of the snippet files."""
    
    def __init__(self):
        self.metadata: Metadata = None
        self.path: Path = None
        """The path where the zipped snippet is saved."""
    
    @property
    def name(self) -> str:
        """The snippet's name."""
        return self.metadata.name
    
    @property
    def id(self) -> str:
        """The snippet's full ID."""
        return self.metadata.id
    
    @property
    def min_id(self) -> str:
        """The snippet's ID, limited to it's minimum length."""
        return self.id[:self.ID_MIN_LEN]
    
    @property
    def description(self) -> str:
        """The snippet's description."""
        return self.metadata.description
    
    @property
    def git_init(self) -> bool:
        """Whether to create a git repository when
        deploying the snippet."""
        return self.metadata.git_init
    
    @property
    def creation_date(self) -> datetime | None:
        """The date when the snippet was created."""
        return self.metadata.creation_date
    
    @classmethod
    def create(cls, origin: Path, name: str = "", description: str = "",
               git_init: bool = True, to: Path | None = None) -> Self:
        """Create a snippet.

        :param Path origin: The path of the directory where the snippet
        to compress is stored.
        :param str name: The snippet's name, defaults to an empty string.
        :param str description: The snippet's description, defaults to ""
        :param bool git_init: Whether to create a git repository when
        deploying the snippet, defaults to True
        :param Path | None to: The path to save the snippet, defaults to
        the assigned path at the project directory.
        :return Self: The created snippet.
        """
        self: Snippet = cls.__new__(cls)
        
        self.metadata = Metadata(name, description, git_init)
        
        if to is not None:
            self.path = to
        else:
            self.path = self.assigned_path()
        
        self._compress(origin, self.path)
        return self
    
    @classmethod
    def load(cls, path: Path) -> Self:
        """Load a built snippet from `path`.

        :param Path path: The path where the built snippet is.
        :return Self: The loaded snippet.
        :raises InvalidSnippetError: When the snippet is invalid.
        """
        if not path.exists():
            logger.error("Invalid snippet at \"%s\".", path)
            raise InvalidSnippetError(path)
        
        self: Snippet = cls.__new__(cls)
        self.path = path
        
        logger.info(f"Loading Snippet from \"{self.path}\".")
        
        with SnippFile(self.path) as file:
            self.metadata = Metadata.extract(file)
        
        return self
    
    def rename(self, new_name: str) -> None:
        """Change the name of the snippet.
        
        This will also change the
        snippet's path and modify it's metadata. To do that, this method
        will extract the snippet in a temporary folder, apply the
        changes and then compress it again, so be careful with renaming
        just because.

        :param str new_name: The new name for the snippet.
        """
        self.metadata.name = new_name
        
        sanitized: str = self.metadata.sanitized_name()
        new_path: Path = self.path.with_stem(sanitized)
        
        if self.path.exists():
            self.path.rename(new_path)
        
        self.path = new_path
        
        with TemporaryDirectory() as temp:
            logger.info("Extracting %r to %r.", self, temp)
            self.extract(temp)
            
            os.remove(self.path)
            logger.info("Removed \"%s\".", self.path)
            
            self._compress(temp, self.path)
    
    def open(self, mode: str = "r") -> SnippFile:
        return SnippFile(self.path, mode)
    
    def namelist(self) -> list[PurePath]:
        """List all the contents inside the snippet.

        :return list[PurePath]: The content list.
        """
        with self.open() as file:
            nl: bytes = file.read_part("file_index")
        
        nl: list[str] = json.loads(nl)
        return [PurePath(path) for path in nl]

    def extract(self, path: Path) -> None:
        """Extract the snippet to `path`.

        :param Path to: The path where the snippet will be extracted.
        """
        logger.info("Extracting %r to \"%s\".", self, path)

        with self.open() as file:
            buffer = io.BytesIO(file.read_part("contents"))
        
        with py7zr.SevenZipFile(buffer) as z7:
            z7.extractall(path)
        
        logger.info("Successfully extracted %r to \"%s\".", self, path)
    
    def _compress(self, origin: Path, to: Path):
        """Compress a directory with the snippet style.

        :param Path origin: The directory path.
        :param Path to: The path where the compressed snippet will be
        saved.
        """
        logger.info("Compressing %r", self)

        with io.BytesIO() as buffer:
            with py7zr.SevenZipFile(buffer, "w") as z7:
                for root, dirs, files in os.walk(origin):
                    for file in files:
                        file_path: Path = Path(root) / file
                        z7.write(file_path, file_path.relative_to(origin))
                
                namelist = z7.namelist()
            
            buffer.seek(0)
            
            with SnippFile(to, "w") as file:
                file.add_metadata(self.metadata)
                file.add_contents(buffer.read())
                file.add_file_index(namelist)
        
        logger.info("Compressed %r", self)

    def assigned_path(self) -> Path:
        """
        Assign a path in the snippets directory based on the sanitized name.
        """
        return SNIPPETS / (self.metadata.sanitized_name() + self.SUFFIX)
    
    def update_contents(self, origin: Path) -> None:
        """Update the contents of a snippet.

        :param Path origin: The path where the new contents are.
        """
        self._compress(origin, self.path)
        
    def __repr__(self) -> str:
        return f"<Snippet name={self.name!r} id={self.id!r} " \
               f"path={self.path!r}>"