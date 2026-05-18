from ..core import *

def main(name: str | None, id: str | None, new_name: str) -> int:
    snippet = find_by(name, id)
    
    old_name = snippet.name
    
    with console.status("Renaming..."):
        snippet.rename(new_name)
    
    print(f"Renamed snippet \"{old_name}\" to \"{snippet.name}\".")
    return 0