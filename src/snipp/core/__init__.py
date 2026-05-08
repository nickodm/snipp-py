from rich.console import Console

__all__ = ["console", "print", "err", "printerr", "paths", "Snippet", "load_snippets",
    "find_by_id"]

from . import paths
from .snippet import Snippet
from .loading import load_snippets, find_by_id

console = Console()
print = console.print

err = Console(stderr=True, style="bold red")
printerr = err.print

