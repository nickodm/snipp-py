from typing import Generator

from . import Snippet
from .paths import SNIPPETS

def load_snippets() -> Generator[Snippet, None, None]:
    """
    Load the saved snippets.

    :yield Snippet:
    """
    if not SNIPPETS.exists():
        return
    
    for entry in SNIPPETS.iterdir():
        loaded = Snippet.load(entry)

        if loaded is not None:
            yield loaded

def find_by_id(id: str) -> Snippet | None:
    """Find and load a snippet by its ID.

    :param str id: The snippet's ID.
    :return Snippet | None: The snippet, if found.
    """
    if len(id) < 5:
        return None
    
    if not SNIPPETS.exists():
        return None
    
    for file in SNIPPETS.iterdir():
        if not file.is_file():
            continue
        
        temp = Snippet.load(file)
        
        if temp is None:
            return None
        
        if temp.uuid.startswith(id):
            return temp
    
    return None

def find_by_name(name: str) -> Snippet | None:
    """Find and load a snippet by its name.

    :param str name: The snippet's name.
    :return Snippet | None: The snippet, if found.
    """
    from .snippet import sanitize_name
    
    if not SNIPPETS.exists():
        return None
    
    name = sanitize_name(name)
    path = SNIPPETS / (name + ".zip")
    
    if not path.exists():
        return None
    
    return Snippet.load(path)

def find_by(name: str | None = None, id: str | None = None) -> Snippet | None:
    """Find and load a snippet by its name or ID.

    :param str | None name: The snippet's name, defaults to None
    :param str | None id: The snippet's id, defaults to None
    :return Snippet | None: The snippet, if found.
    """
    if id:
        return find_by_id(id)
    else:
        return find_by_name(name)