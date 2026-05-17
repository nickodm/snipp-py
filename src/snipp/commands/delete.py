from ..core import *
from os import remove

def main(id: str) -> int:
    snippet = find_by_id(id)

    if snippet is None:
        printerr("Snippet not found.")
        return 1
    try:
        remove(snippet.path)
    except PermissionError:
        printerr("Error: The file is being used or the process has no "
                 "permission to delete it.")
        return 1
    
    print(f"Removed snippet \"{snippet.name}\".")
    return 0