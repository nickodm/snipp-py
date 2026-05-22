from pathlib import Path
import logging as _logging

from ..core import *
from ..core.errors import SnippetNotFoundError
from ..core.parser import *

logger = _logging.getLogger(__name__)

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
    
    try:
        snippet = find_by_name(name)
        logger.critical("Repeated name: %s", name)
        printerr("There is already a snippet with this name.")
        return 1
    except SnippetNotFoundError:
        pass
    
    with console.status("Creating..."):
        logger.info("Creating snippet from \"%s\".", path)
        snippet = Snippet.create(path, name, description, git, to)

    logger.info("Created snippet %r, saved to %s", snippet, to)
    print(f":white_check_mark: Created snippet \"{snippet.name}\".")
    
    if to is not None:
        print(f"Saved to \"{snippet.path}\".")
    
    return 0

@command_register
def register(cmds: SubParser) -> None:
    create = cmds.add_parser(
        name="create",
        help="create a snippet from a directory",
        description="Create a snippet from a directory.")
    create.add_argument("name", type=str)
    
    create.register("type", "path", type_path)
    
    exclusive = create.add_mutually_exclusive_group()
    exclusive.add_argument("-d", "--description", type=str, default='',
        help="add a description to the snippet")
    exclusive.add_argument("-D", "--description-file", type="path", dest="description_file",
        help="read the description from a file", metavar="PATH")
    
    create.add_argument("-p", "--path", type="path", default=Path.cwd(),
        help="the path where the snippet is (defaults to current working directory)")
    create.add_argument("--no-git", action="store_false", dest="git",
        help="don't init a git repository when using the use command")
    create.add_argument("--save-to", type="path", dest="to", metavar="PATH",
        help="specify a different path to save the snippet")
    
    create.set_defaults(func=main)