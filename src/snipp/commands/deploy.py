from pathlib import Path
from subprocess import run

from ..core import *

def dir_is_empty(path: Path) -> bool:
    for _ in path.iterdir():
        return False
    
    return True

def git_init(path: Path) -> bool:
    """Create a git repository at `path`.

    :param Path path: The path where the git repository will be created.
    :return bool: Whether the git repository was created.
    """
    try:
        return run(["git", "init"], cwd=path, capture_output=True) \
            .returncode == 0
    except FileNotFoundError:
        return False

def main(name: str | None, id: str | None, path: Path, force: bool) -> int:
    snippet = find_by(name, id)
    
    if snippet is None:
        printerr("Snippet not found.")
        return 1
    
    if path.is_file():
        printerr("Error: Can't deploy to a file.")
        return 1
    
    if not force and path.is_dir() and not dir_is_empty(path):
        printerr("Error: The directory is not empty.")
        return 1
   
    with console.status(f"Deploying snippet \"{snippet.name}\"..."):
        snippet.extract(path)
        
        if snippet.git_init:
            if git_init(path):
                print("Created git repository.")
            else:
                printerr("Cannot create git repository.")
    
    print(":white_check_mark: [green]Snippet deployed successfully.")
    return 0