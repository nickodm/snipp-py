from ..core import *
from os import remove

def main(name: str | None, id: str | None) -> int:
    snippet = find_by(name, id)
    
    try:
        remove(snippet.path)
    except PermissionError:
        printerr("Error: The file is being used or the process has no "
                 "permission to delete it.")
        return 1
    
    print(f"Removed snippet \"{snippet.name}\".")
    return 0