from pathlib import Path

from ..core import *

def main(name: str | None, id: str | None, path: Path, force: bool) -> int:
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

    if path.suffix == "" or path.is_dir():
        path = path.joinpath(snippet.metadata.sanitized_name() + ".zip")

    if not force and path.exists() and path.is_file():
        printerr(f"Error: The file \"{path}\" already exists.")
        return 1
    
    with console.status("Exporting..."):
        with open(snippet.path, "rb") as zf:
            read = zf.read()
        
        with open(path, "wb") as fp:
            fp.write(read)

    print(":white_check_mark: [green]Snippet exported successfully.")
    return 0