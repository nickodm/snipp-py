from ..core import *

def main(name: str | None, id: str | None, new_name: str) -> int:
    if name is None and id is None:
        printerr("Error: You must specify a name or an id.")
        return 1
    
    if id:
        snippet = find_by_id(id)
    else:
        snippet = find_by_name(name)

    if not snippet:
        printerr("Snippet not found.")
        return 1
    
    old_name = snippet.name
    
    with console.status("Renaming..."):
        snippet.rename(new_name)
    
    print(f"Renamed snippet \"{old_name}\" to \"{snippet.name}\".")
    return 0