from pathlib import Path

from ..core import *

def read_description(path: Path) -> str:
    if not path.exists():
        printerr("Error: The description file doesn't exists.")
        exit(1)

    if not path.is_file():
        printerr("Error: The description file is not a file.")
        exit(1)
    
    try:
        with path.open() as fp:
            return fp.read()
    except UnicodeDecodeError:
        printerr("Error: The file is a binary.")
        exit(1)

def main(path: Path, name: str, description: str, git: bool, to: Path | None,
         description_file: Path | None) -> int:
    if description_file:
        description = read_description(description_file)
    
    snippet = Snippet.create(path, name, description, git)
    print(f"Created snippet \"{snippet.name}\".")
    with console.status("Saving..."):
        snippet.save()
    return 0