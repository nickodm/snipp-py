from pathlib import Path
from zipfile import ZipFile
from uuid import uuid4
from datetime import datetime
import tomlkit as t
import os

from .paths import SNIPPETS

# TODO: Validate with regex
def sanitize_name(name: str) -> str:
    replace_pairs = {
        " ": "_",
        "ñ": "n",
        "+": ""
    }
    
    return name.lower() \
               .replace(" ", "_") \
               .replace("ñ", "n")

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
        self.path: Path | None = None
        """The path where the zipped snippet is saved."""
        self.origin: Path | None = None
        """The origin of the Snippet."""
    
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
               git_init: bool = True) -> 'Snippet':
        """Create a snippet based on the folder at `path`.

        :param Path path: _description_
        :return Snippet: _description_
        """
        self: Snippet = cls.__new__(cls)
        
        self.origin = origin
        self.metadata = Metadata(name, description, git_init)
        self._assign_path()
        
        # self.save()
        return self
    
    @classmethod
    def load(cls, path: Path) -> 'Snippet':
        """Load a built snippet from `path`.

        :param Path path: The path where the built snippet is.
        :return Snippet: The loaded snippet.
        """
        self: Snippet = cls.__new__(cls)
        self.path = path
        
        with ZipFile(path) as zf:
            self.metadata = Metadata.extract(zf)
        
        return self
    
    def rename(self, new_name: str) -> None:
        self.metadata.name = new_name
        
        sanitized: str = self.metadata.sanitized_name()
        new_path: Path = self.path.with_stem(sanitized)
        
        if self.path.exists():
            self.path.rename(new_path)
        
        self.path = new_path

    def save(self, to: Path | None = None) -> None:
        """Save the snippet to the directory.

        :param Path | None to: _description_, defaults to None
        """
        
        if to is None:
            to = self.path
        
        if not self.origin:
            return None
        
        with ZipFile(to, "w") as zf:
            zf.writestr(Metadata.FILENAME, self.metadata.as_toml())

            for item, _, files in os.walk(self.origin):
                item = Path(item)
                for file in files:
                    file_path: Path = item / file
                    zf.write(file_path, Path("contents") / file_path.relative_to(self.origin))
        
        return None
    
    def open(self, mode: str = "r") -> ZipFile:
        return ZipFile(self.path, mode)
    
    def namelist(self) -> list[Path]:
        nl: list[str] = []
        with self.open() as zf:
            nl = zf.namelist()
        
        buffer: list[Path] = []
        for path in nl:
            path = Path(path)
            
            if not path.is_relative_to("contents"):
                continue
            
            buffer.append(path.relative_to("contents"))
        
        return buffer

    def extract(self, path: Path | None = None):
        """Extract the snippet to `path`.

        :param Path | None to: _description_, defaults to None
        :return _type_: _description_
        """
        if path is None and self.origin is None:
            # sofrimento eterno
            return NotImplemented

        if path is None:
            path = self.origin
        
        with ZipFile(self.path) as z:
            z.extractall(path, ["contents"])
        
        os.remove(path / Metadata.FILENAME)

    def _assign_path(self) -> None:
        """
        Assign a path in the snippets directory based on the sanitized name.
        """
        self.path = SNIPPETS / (self.metadata.sanitized_name() + ".zip")
        
    def __repr__(self) -> str:
        return f"Snippet(name={self.name}, path={self.path}, origin={self.origin})"