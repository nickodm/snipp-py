from pathlib import Path

from ..core import *

def main(path: Path, update: bool) -> int:
    if not path.exists():
        printerr("Error: The path doesn't exists.")
        return 1
    
    if path.is_dir():
        printerr("Error: The path is a dir.")
        return 1
    
    snippet = Snippet.load(path)
    
    if snippet is None:
        printerr("Error: Invalid snippet.")
        return 1
    
    if not update and already_stored(snippet):
        printerr("The snippet is already stored "
                 f"(id [blue]{snippet.uuid[:5]}[/blue]).")
        return 1
    
    snippet.path = snippet.assigned_path()
    with console.status("Importing..."):
        with open(path, "rb") as fp:
            read = fp.read()
        
        with open(snippet.path, "wb") as fp:
            fp.write(read)
    
    print(f":white_check_mark: Imported snippet \"{snippet.name}\".")
    return 0