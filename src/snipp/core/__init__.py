from rich.console import Console

__all__ = [
    #* Generals
    "console", "print", "paths", "Snippet",
    
    #* Loading
    "load_snippets", "find_by_id", "find_by_name", "find_by", "already_stored",
    
    #* Errors
    "SnippError", "err", "printerr"
]

from . import paths
from .snippet import Snippet
from .loading import load_snippets, find_by_id, find_by_name, find_by
from .errors import *

console = Console()
print = console.print

def already_stored(snippet: Snippet) -> bool:
    """Whether the snippet is already stored.

    :param Snippet snippet: The snippet to verify.
    :return bool:
    """
    for snipp in load_snippets():
        if snipp.id == snippet.id:
            return True
    
    return False