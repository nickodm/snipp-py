from pathlib import Path
from platformdirs import PlatformDirs

__all__ = ["SNIPPETS", "TEMP"]

dirs = PlatformDirs("snipp", "NickoDM", ensure_exists=True, roaming=True)

SNIPPETS: Path = dirs.user_data_path / "snippets"
"""The directory where the snippets are saved."""

TEMP: Path = dirs.user_runtime_path
"""The directory where the temporary files are saved."""

def init_project_dir() -> None:
    """Create all the project directories that should exist for the
    correct execution of the program.
    """
    paths = [SNIPPETS]
    
    for path in paths:
        if not path.exists():
            path.mkdir()