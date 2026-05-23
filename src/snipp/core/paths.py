from pathlib import Path
from platformdirs import PlatformDirs
from importlib import resources

import logging

logger = logging.getLogger(__name__)

__all__ = ["SNIPPETS", "TEMP"]

dirs = PlatformDirs("snipp", "NickoDM", ensure_exists=True, roaming=True)

SNIPPETS: Path = dirs.user_data_path / "snippets"
"""The directory where the snippets are saved."""

TEMP: Path = dirs.user_runtime_path
"""The directory where the temporary files are saved."""

LOGS: Path = dirs.user_log_path
"""The directory where the logs will be saved."""

lastlog_path: Path = LOGS / "last.log"
"""The path of the last log file."""

ASSETS = resources.files("snipp.assets")
"""The traversable where the program's resources are."""

def init_project_dir() -> None:
    """Create all the project directories that should exist for the
    correct execution of the program.
    """
    paths = [SNIPPETS]
    
    logger.info("Initializing project directories...")
    for path in paths:
        if not path.exists():
            path.mkdir()
            logger.info(f"Created \"{path}\".")