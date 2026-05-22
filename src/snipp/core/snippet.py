from pathlib import Path, PurePath
from pathvalidate import sanitize_filename
from zipfile import ZipFile, is_zipfile
from uuid import uuid4
from datetime import datetime
from tempfile import TemporaryDirectory, NamedTemporaryFile
from typing import Generator
import tomlkit as t
import logging as _logging
import json
import shutil
import os

from .paths import SNIPPETS, TEMP
from .errors import *

from snipp import __version_info__

logger = _logging.getLogger(__name__)

def relatives(path: Path) -> Generator[tuple[PurePath, PurePath], None, None]:
    """Walk over the directory at `path` and yield tuples with the
    relative path and the absolute path of each file.
    
    :param Path path: The directory to walk in.
    :yield tuple[PurePath, PurePath]: The tuple `(relative, file_path)`.
    """
    # {relative: original}
    for item, _, files in os.walk(path):
        item = PurePath(item)
        
        for file in files:
            file_path: PurePath = item / file
            relative = file_path.relative_to(path)
            yield (relative, file_path)


class Metadata:
    """
    A class representing the metadata of a snippet.
    """
    
    FILENAME: str = "metadata.json"
    """The name of the metadata file inside the snippet."""
    
    def __init__(self, name: str, description: str = "", git_init: bool = True):
        self.name: str = name
        self.id: str = str(uuid4())
        self.description: str = description
        self.git_init: bool = git_init
        self.creation_date: datetime | None = datetime.now()
        self.software_version: tuple[int, int, int] = __version_info__
        
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
    
    def as_json(self, *, 
                indent: int | None = 4) -> str:
        """Dump the metadata as a JSON.
        
        :param int | None indent: The indentation for the JSON,
        defaults to 4
        
        :return str: The metadata as a JSON.
        """
        
        data = {
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
        
        return json.dumps(data, indent=indent)
    
    @classmethod
    def from_dict(cls, d: dict) -> 'Metadata':
        """Load a snippet's metadata from a dictionary.

        :param dict d: The dictionary.
        :return Metadata: The loaded metadata.
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
    def from_toml(cls, source: str | bytes) -> 'Metadata':
        """Parse the metadata information from a TOML string.

        :param str | bytes source: The TOML as a string or bytes.
        :return Metadata: The loaded metadata.
        """
        return cls.from_dict(t.parse(source))
    
    @classmethod
    def from_json(cls, source: str | bytes) -> 'Metadata':
        """Parse the metadata information from a JSON string.

        :param str | bytes source: The JSON as a string or bytes.
        :return Metadata: The loaded metadata.
        """
        data: dict = json.loads(source)
        info = data["snippet-info"]
        info["creation_date"] = datetime.fromordinal(info["creation_date"])
        return cls.from_dict(data)
    
    @classmethod
    def extract(cls, zf: ZipFile) -> 'Metadata':
        """Extract the metadata of a snippet from an opened ZipFile.

        :param ZipFile zf: The opened ZipFile.
        :return Metadata: The extracted metadata.
        """
        return cls.from_json(zf.read(cls.FILENAME))
    
    def write(self, zf: ZipFile) -> None:
        """Write the metadata of a snippet to a **opened** ZipFile.

        :param ZipFile zf: The opened zipfile.
        """
        return zf.writestr(self.FILENAME, self.as_json())


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
               git_init: bool = True, to: Path | None = None) -> 'Snippet':
        """Create a snippet.

        :param Path origin: The path of the directory where the snippet
        to compress is stored.
        :param str name: The snippet's name, defaults to an empty string.
        :param str description: The snippet's description, defaults to ""
        :param bool git_init: Whether to create a git repository when
        deploying the snippet, defaults to True
        :param Path | None to: The path to save the snippet, defaults to
        the assigned path at the project directory.
        :return Snippet: The created snippet.
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
    def load(cls, path: Path):
        """Load a built snippet from `path`.

        :param Path path: The path where the built snippet is.
        :return Snippet | None: The loaded snippet.
        :raises InvalidSnippetError: When the snippet is invalid.
        """
        if not cls._is_valid(path):
            logger.error("Invalid snippet at \"%s\".", path)
            raise InvalidSnippetError(path)
        
        self: Snippet = cls.__new__(cls)
        self.path = path
        
        logger.info(f"Loading Snippet from \"{self.path}\".")
        with self.open() as zf:
            self.metadata = Metadata.extract(zf)
        
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
            with self.open() as zf:
                zf.extractall(temp)
            
            os.remove(self.path)
            
            self._compress(temp, self.path, raw=True)
    
    def open(self, mode: str = "r") -> ZipFile:
        return ZipFile(self.path, mode)
    
    def namelist(self) -> list[PurePath]:
        """List all the contents inside the snippet.

        :return list[PurePath]: The content list.
        """
        nl: list[str] = []
        with self.open() as zf:
            nl = zf.namelist()
        
        buffer: list[PurePath] = []
        for path in nl:
            path = PurePath(path)
            
            if not path.is_relative_to("contents"):
                continue
            
            buffer.append(path.relative_to("contents"))
        
        return buffer

    def extract(self, path: Path) -> None:
        """Extract the snippet to `path`.

        :param Path to: The path where the snippet will be extracted.
        """
        logger.info("Extracting %r to \"%s\".", self, path)
        with ZipFile(self.path) as z:
            for file in self.namelist():
                destiny: Path = path.joinpath(file)
                buffer: bytes = z.read("contents/" + file.as_posix())
                
                if not destiny.parent.exists():
                    destiny.parent.mkdir(parents=True)
                
                with open(destiny, "wb") as fp:
                    fp.write(buffer)
        logger.info("Successfully extracted %r to \"%s\".", self, path)
    
    def _compress(self, origin: Path, to: Path, *, raw: bool = False):
        """Compress a directory with the snippet style.

        :param Path origin: The directory path.
        :param Path to: The path where the compressed snippet will be
        saved.
        :param bool raw: If true, the directory will be compressed as-is,
        without the snippet format.
        """
        logger.info("Compressing %r", self)
        with NamedTemporaryFile(delete=False, suffix=".zip", dir=TEMP) as temp_file:
            temp_path: Path = Path(temp_file.name)

            with ZipFile(temp_file, "w") as zf:
                if not raw:
                    self.metadata.write(zf)

                for relative, original in relatives(origin):
                    if not raw:
                        relative = PurePath("contents") / relative
                    
                    zf.write(original, relative)
        
        shutil.move(temp_path, to)
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
        
    @staticmethod
    def _is_valid(path: Path) -> bool:
        """Whether the file at `path` is a valid snippet or not.

        :param Path path: The path of the supposed snippet.
        :return bool: Whether the file is a valid snippet.
        """
        if not path.exists():
            return False
        
        if not is_zipfile(path):
            return False
        
        with ZipFile(path) as zf:
            if zf.testzip() is not None:
                return None
            
            namelist: list[str] = zf.namelist()
        
        if not Metadata.FILENAME in namelist:
            return False
        
        return True
        
    def __repr__(self) -> str:
        return f"Snippet(name={self.name!r}, id={self.id!r}, " \
               f"path={self.path!r})"