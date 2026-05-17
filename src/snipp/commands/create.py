from pathlib import Path

from ..core import *

def read_description(path: Path) -> str:
    """read the description from a file.

    :param Path path: The file's path.
    :return str: The read description.
    """
    if not path.exists():
        printerr("Error: The description file doesn't exists.")
        exit(1)

    if not path.is_file():
        printerr("Error: The description file is not a file.")
        exit(1)
    
    try:
        with path.open(encoding="utf-8") as fp:
            return fp.read()
    except UnicodeDecodeError:
        printerr("Error: The description file is a binary.")
        exit(1)

def main(path: Path, name: str, description: str, git: bool, to: Path | None,
         description_file: Path | None) -> int:
    if description_file:
        description = read_description(description_file)
    
    snippet = Snippet.create(path, name, description, git)
    print(f"Created snippet \"{snippet.name}\".")
    
    msg = "Saving..." if to is None else f"Saving to \"{to}\"..."
    with console.status(msg):
        saved = snippet.save(to)

    print(f"Saved to \"{saved}\".")
    return 0