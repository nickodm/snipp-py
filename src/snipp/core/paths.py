from pathlib import Path

__all__ = ["PROJECT_DIR", "SNIPPETS"]

PROJECT_DIR: Path = Path("~/.snipp").expanduser()
SNIPPETS: Path = PROJECT_DIR.joinpath("snippets")

def init_project_dir():
    PROJECT_DIR.joinpath("snippets")