import logging as _logging

from ..core import *
from ..core.errors import SnippetNotFoundError
from ..core.parser import *

logger = _logging.getLogger(__name__)

def main(name: str | None, id: str | None, new_name: str) -> int:
    try:
        snippet = find_by_name(new_name)
        logger.critical("Repeated name: %s", name)
        printerr("There is already a snippet with this name.")
        return 1
    except SnippetNotFoundError:
        pass
    
    snippet = find_by(name, id)
    
    old_name = snippet.name
    
    logger.info("Renaming %r", snippet)
    with console.status("Renaming..."):
        snippet.rename(new_name)
    
    logger.info("Renamed %r", snippet)
    print(f"Renamed snippet \"{old_name}\" to \"{snippet.name}\".")
    return 0

@command_register
def register(cmds: SubParser) -> None:
    rename = cmds.add_parser(
        name="rename",
        help="change a snippet's name",
        description="Change a snippet's name."
    )
    
    exclusive = rename.add_mutually_exclusive_group(required=True)
    
    exclusive.add_argument("-n", "--name", type=str, 
        help="the name of the snippet to rename")
    exclusive.add_argument("-i", "--id", type=str,
        help="the ID of the snippet to rename")
    
    rename.add_argument("new_name",
        help="the new name for the snippet")
    
    rename.set_defaults(func=main)