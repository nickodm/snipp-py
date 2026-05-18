from pathlib import Path
from rich.console import Console

from . import ID_MIN_LEN

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
    def __init__(self, path: Path):
        super().__init__(f"The snippet at \"{path}\" is not valid.")

class IDTooShortError(SnippError):
    """The provided ID is too short to recognize a snippet."""
    exit_code: int = 2
    def __init__(self, id: str):
        super().__init__(f"The ID is too short (minimum {ID_MIN_LEN}, "
                         f"got {len(id)}).")