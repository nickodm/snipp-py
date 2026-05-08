

from . import Snippet
from .paths import SNIPPETS

def load_snippets():
    """
    Load the saved snippets.

    :yield Snippet:
    """
    if not SNIPPETS.exists():
        return
    
    for entry in SNIPPETS.iterdir():
        yield Snippet.load(entry)

def find_by_id(id: str) -> Snippet | None:
    if len(id) < 5:
        return None
    
    if not SNIPPETS.exists():
        return None
    
    for file in SNIPPETS.iterdir():
        if not file.is_file():
            continue
        
        temp = Snippet.load(file)
        
        if temp.uuid.startswith(id):
            return temp
    
    return None