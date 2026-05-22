from pathlib import Path
from subprocess import run
import logging as _logging

from ..core import *
from ..core.parser import *

logger = _logging.getLogger(__name__)

def dir_is_empty(path: Path) -> bool:
    for _ in path.iterdir():
        return False
    
    return True

def git_init(path: Path) -> bool:
    """Create a git repository at `path`.

    :param Path path: The path where the git repository will be created.
    :return bool: Whether the git repository was created.
    """
    logger.info("Creating git repository at \"%s\"", path)
    try:
        return run(["git", "init"], cwd=path, capture_output=True) \
            .returncode == 0
    except FileNotFoundError:
        logger.exception("Could not create git repository.")
        return False

def main(name: str | None, id: str | None, path: Path, force: bool) -> int:
    snippet = find_by(name, id)
    
    logger.info("Deploying snippet %r", snippet)
    
    if path.is_file():
        logger.critical("Tried to deploy to a file.")
        printerr("Error: Can't deploy to a file.")
        return 1
    
    if not force and path.is_dir() and not dir_is_empty(path):
        logger.critical("Tried to deploy to a not empty directory.")
        printerr("Error: The directory is not empty.")
        return 1
   
    with console.status(f"Deploying snippet \"{snippet.name}\"..."):
        snippet.extract(path)
        
        if snippet.git_init:
            if git_init(path):
                print("Created git repository.")
            else:
                printerr("Cannot create git repository.")
    
    logger.info("Snippet deployed successfully.")
    print(":white_check_mark: Snippet deployed successfully.")
    return 0

@command_register
def register(cmds: SubParser) -> None:
    deploy = cmds.add_parser(
        name="deploy",
        help="deploy a snippet",
        description="Deploy a snippet."
    )
    
    deploy.register("type", "path", type_path)
    
    exclusive = deploy.add_mutually_exclusive_group(required=True)
    
    exclusive.add_argument("-n", "--name", type=str, 
        help="the name of the snippet to deploy")
    exclusive.add_argument("-i", "--id", type=str,
        help="the ID of the snippet to deploy")
    
    deploy.add_argument("-p", "--path", type="path", default=Path.cwd(),
        help="the path where the snippet will be deployed. Defaults to "
             "the current working directory.")
    deploy.add_argument("-f", "--force", action="store_true",
        help="force the snippet creation")
    
    deploy.set_defaults(func=main)