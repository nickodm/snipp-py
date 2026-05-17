from pathlib import Path, PurePath
from zipfile import ZipFile
from uuid import uuid4
from datetime import datetime
from tempfile import TemporaryDirectory
import re
import tomlkit as t
import os

from .paths import SNIPPETS

def validate_name(name: str) -> bool:
    """Validate a Snippet's name.

    :param str name: The name to validate.
    :return bool: Whether the snippet is valid or not.
    """
    return re.match(r"^[\w_]+$", name) is not None

# TODO: Validate with regex
def sanitize_name(name: str) -> str:
    if not validate_name(name):
        raise ValueError(f"\"{name}\" is not a valid name.")
    
    replace_pairs = {
        " ": "_",
        "ñ": "n",
        "+": ""
    }
    
    name = name.lower()
    for old, new in replace_pairs.items():
        name = name.replace(old, new)
    
    return name

class Metadata:
    """
    A class representing the metadata of a snippet.
    """
    
    FILENAME: str = "metadata.toml"
    
    def __init__(self, name: str, description: str = "", git_init: bool = True):
        self.name: str = name
        self.uuid: str = str(uuid4())
        self.description: str = description
        self.git_init: bool = git_init
        self.creation_date: datetime | None = datetime.now()
        
    def sanitized_name(self) -> str:
        return sanitize_name(self.name)
        
    def as_toml(self) -> str:
        """Render the metadata information as a TOML.

        :return str: The TOML as a string.
        """
        doc = t.document()
        
        info = t.table()
        info.add(t.comment("The name to display."))
        info.add("name", self.name)
        
        info.add(t.comment("DO NOT TOUCH!"))
        info.add("uuid", self.uuid)
        
        info.add(t.comment("The description of the snippet."))
        info.add("description", self.description)
        
        info.add(t.comment("Whether to init a git repository when using the snippet."))
        info.add("git_init", self.git_init)
        
        info.add(t.comment("The date when the snippet was created."))
        info.add("creation_date", self.creation_date)
        
        doc.add("snippet-info", info)
        
        return doc.as_string()
    
    @classmethod
    def from_toml(cls, toml: str | bytes) -> 'Metadata':
        """Parse the metadata information from a TOML string.

        :param str | bytes toml: The TOML as a string or bytes.
        :return Metadata: The loaded metadata.
        """
        self: Metadata = cls.__new__(cls)

        loaded = t.parse(toml)
        info: dict = loaded.get("snippet-info", {})
        
        self.name = info.get("name", "[Unnamed]")
        self.uuid = info.get("uuid", str(uuid4()))
        self.description = info.get("description", "")
        self.git_init = info.get("git_init", True)
        self.creation_date = info.get("creation_date", None)
        return self
    
    @classmethod
    def extract(cls, zf: ZipFile) -> 'Metadata':
        """Extract the metadata of a snippet from an opened ZipFile.

        :param ZipFile zf: The opened ZipFile.
        :return Metadata: The extracted metadata.
        """
        return cls.from_toml(zf.read(cls.FILENAME))


class Snippet:
    def __init__(self):
        self.metadata: Metadata = None
        self.path: Path = None
        """The path where the zipped snippet is saved."""
    
    @property
    def name(self) -> str:
        return self.metadata.name
    
    @property
    def uuid(self) -> str:
        return self.metadata.uuid
    
    @property
    def description(self) -> str:
        return self.metadata.description
    
    @property
    def git_init(self) -> bool:
        return self.metadata.git_init
    
    @property
    def creation_date(self) -> datetime | None:
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
            self.path = self._assigned_path()
        
        self._compress(origin, self.path)
        return self
    
    @classmethod
    def load(cls, path: Path):
        """Load a built snippet from `path`.

        :param Path path: The path where the built snippet is.
        :return Snippet | None: The loaded snippet.
        """
        self: Snippet = cls.__new__(cls)
        self.path = path
        self.origin = None
        
        with ZipFile(path) as zf:
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
        with ZipFile(self.path) as z:
            for file in self.namelist():
                destiny: Path = path.joinpath(file)
                buffer: bytes = z.read("contents/" + file.as_posix())
                
                if not destiny.parent.exists():
                    destiny.parent.mkdir(parents=True)
                
                with open(destiny, "wb") as fp:
                    fp.write(buffer)
    
    def _compress(self, origin: Path, to: Path, *, raw: bool = False):
        """Compress a directory with the snippet style.

        :param Path origin: The directory path.
        :param Path to: The path where the compressed snippet will be
        saved.
        :param bool raw: If true, the directory will be compressed as-is,
        without the snippet format.
        """
        
        # {relative: original}
        buffer: dict[str, Path] = {}
        for item, _, files in os.walk(origin):
            item = Path(item)
            
            for file in files:
                file_path: Path = item / file
                relative = file_path.relative_to(origin).as_posix()
                buffer[relative] = file_path
        
        if raw:
            with ZipFile(to, "w") as zf:
                for relative, original in buffer.items():
                    zf.write(original, relative)
        else:
            with ZipFile(to, "w") as zf:
                zf.writestr(Metadata.FILENAME, self.metadata.as_toml())

                for relative, original in buffer.items():
                    zf.write(original, PurePath("contents") / relative)

    def _assigned_path(self) -> Path:
        """
        Assign a path in the snippets directory based on the sanitized name.
        """
        return SNIPPETS.joinpath(self.metadata.sanitized_name() + ".zip")
        
    def __repr__(self) -> str:
        return f"Snippet(name={self.name}, path={self.path})"