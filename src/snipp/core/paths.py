from pathlib import Path

__all__ = ["BASE_DIR", "SNIPPETS"]

BASE_DIR: Path = Path("~/.snipp").expanduser()
"""The base program's directory."""

SNIPPETS: Path = BASE_DIR / "snippets"
"""The directory where the snippets are saved."""

def init_project_dir() -> None:
    """Create all the project directories that should exist for the
    correct execution of the program.
    """
    paths = [BASE_DIR, SNIPPETS]
    
    for path in paths:
        if not path.exists():
            path.mkdir()