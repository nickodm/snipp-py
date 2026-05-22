from os import remove
import logging as _logging

from ..core import *
from ..core.parser import *

logger = _logging.getLogger(__name__)

def main(name: str | None, id: str | None) -> int:
    snippet = find_by(name, id)
    
    logger.info("Removing snippet %r.", snippet)
    try:
        remove(snippet.path)
    except PermissionError:
        printerr("Error: The file is being used or the process has no "
                 "permission to delete it.")
        logger.exception("Cannot remove %r", snippet)
        return 1
    
    logger.info(f"Removed snippet {snippet}.")
    print(f"Removed snippet \"{snippet.name}\".")
    return 0

@command_register
def register(cmds: SubParser) -> None:
    delete = cmds.add_parser(
        name="remove",
        help="remove a snippet",
        description="Remove a saved snippet."
    )
    
    exclusive = delete.add_mutually_exclusive_group(required=True)
    
    exclusive.add_argument("-n", "--name", type=str, 
        help="the name of the snippet to remove")
    exclusive.add_argument("-i", "--id", type=str,
        help="the ID of the snippet to remove")
    
    delete.set_defaults(func=main)