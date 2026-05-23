from pathlib import Path
from rich.console import Console
import os

err = Console(stderr=True, style="red")
printerr = err.print

class SnippError(Exception):
    """Base class for Snipp exceptions."""
    exit_code: int = 1

class SnippetNotFoundError(SnippError):
    """The snippet was not found in the program's directory."""
    def __init__(self):
        super().__init__("Snippet was not found.")

class InvalidSnippetError(SnippError):
    """The snippet at `path` is invalid."""
    
    if os.name == "nt":
        exit_code = 13
    else:
        exit_code = 65

    def __init__(self, path: Path | None = None):
        if path:
            msg = f"The snippet at \"{path}\" is not valid."
        else:
            msg = "Invalid snippet."
        
        super().__init__(msg)

class InvalidMetadataError(InvalidSnippetError):
    """The metadata of a snippet is not valid."""
    def __init__(self):
        super().__init__(path=None)
        super(SnippError, self).__init__(self.args[0][:-1] \
                                         + ": Invalid metadata.")

class IDTooShortError(SnippError):
    """The provided ID is too short to recognize a snippet."""
    exit_code: int = 2
    def __init__(self, id: str):
        from .snippet import Snippet # prevent circular import
        super().__init__(f"The ID is too short (minimum {Snippet.ID_MIN_LEN}, "
                         f"got {len(id)}).")