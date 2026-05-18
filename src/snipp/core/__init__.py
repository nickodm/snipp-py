from rich.console import Console

__all__ = ["console", "print", "err", "printerr", "paths", "Snippet", "load_snippets",
    "find_by_id", "find_by_name", "already_stored"]

from . import paths
from .snippet import Snippet
from .loading import load_snippets, find_by_id, find_by_name

console = Console()
print = console.print

err = Console(stderr=True, style="bold red")
printerr = err.print

def already_stored(snippet: Snippet) -> bool:
    """Whether the snippet is already stored.

    :param Snippet snippet: The snippet to verify.
    :return bool:
    """
    for snipp in load_snippets():
        if snipp.uuid == snippet.uuid:
            return True
    
    return False