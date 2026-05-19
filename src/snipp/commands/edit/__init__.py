from pathlib import Path
from subprocess import run
import json
import os

from ...core import *
from ...core.errors import SnippetNotFoundError, IDTooShortError
from ...core.parser import *

"""
snipp edit start (-n NAME | -i ID)
snipp edit done
snipp edit abort
snipp edit open
"""

def open_in_editor(path: Path) -> bool:
    """Open the path in the $EDITOR environment variable, if exists.

    :param Path path: The path to open.
    :return bool: Whether the action was successfull.
    """
    editor = os.environ.get("EDITOR")

    if editor is None:
        return False
    
    try:
        return run(f"{editor} {path}", capture_output=False).returncode == 0
    except (RuntimeError, FileNotFoundError):
        printerr("Error: Cannot open the directory with the editor.")
        return False

def get_lock_path(snippet: Snippet) -> Path:
    """Get the path of the snippet's lock file.

    :param Snippet snippet:
    :return Path:
    """
    return paths.TEMP \
        .joinpath(snippet.metadata.sanitized_name()) \
        .with_suffix(".lock")
        
def get_temp_dir(snippet: Snippet) -> Path:
    return paths.TEMP \
        .joinpath(snippet.metadata.sanitized_name())

def lock(snippet: Snippet) -> None:
    """Lock the snippet.

    :param Snippet snippet: The snippet to lock.
    """
    path: Path = get_lock_path(snippet)
    
    with open(path, "w") as fp:
        json.dump({
            "id": snippet.uuid,
            "pointer": get_temp_dir(snippet).as_posix()
        }, fp)
    
def unlock(snippet: Snippet) -> None:
    """Unlock the snippet.

    :param Snippet snippet: The snippet to unlock.
    """
    if not is_locked(snippet):
        return
    
    get_lock_path(snippet).unlink(True)

def is_locked(snippet: Snippet) -> bool:
    """Check whether a snippet is already locked.

    :param Snippet snippet: The snippet to check.
    :return bool: Whether the snippet is locked.
    """
    path = get_lock_path(snippet)
    
    if not path.exists():
        return False
    
    with open(path) as fp:
        data: dict = json.load(fp)
    
    if not isinstance(data, dict):
        return False
    
    id = data.get("id")
    
    if id is None:
        return False
    
    return snippet.uuid == id

def find_locked() -> Snippet | None:
    """Find and load the locked snippet, if exists.

    :return Snippet | None: The locked snippet, if found.
    """
    dir: Path = paths.dirs.user_runtime_path
    lockfile: Path | None = None
    
    for item in dir.iterdir():
        if item.is_file() and item.suffix == ".lock":
            lockfile = item
            break
    
    if lockfile is None:
        return None
    
    try:
        with open(lockfile) as fp:
            data: dict = json.load(fp)
    except json.JSONDecodeError:
        lockfile.unlink()
        return None
    
    if not (isinstance(data, dict) and "id" in data):
        return None
    
    try:
        snippet = find_by_id(data["id"])
    except SnippetNotFoundError:
        return None
    except IDTooShortError:
        lockfile.unlink()
        return None
    
    return snippet
    

from . import main as _main