from pathlib import Path
import logging

from ..core import *
from ..core.parser import *

logger = logging.getLogger(__name__)

def main(name: str | None, id: str | None, path: Path, force: bool) -> int:
    snippet = find_by(name, id)

    logger.info("Exporting %r to \"%s\".", snippet, path)
    
    if path.suffix == "" or path.is_dir():
        path = path.joinpath(snippet.path.name)

    if not force and path.exists() and path.is_file():
        logger.critical("Path already exists.")
        printerr(f"Error: The file \"{path}\" already exists.")
        return 1
    
    with console.status("Exporting..."):
        logger.info("Reading snippet bytes...")
        with open(snippet.path, "rb") as zf:
            read = zf.read()
        
        logger.info("Writing snippet bytes...")
        with open(path, "wb") as fp:
            fp.write(read)

    logger.info("Snippet exported successfully.")    
    print(":white_check_mark: Snippet exported successfully.")
    return 0

@command_register
def register(cmds: SubParser) -> None:
    export = cmds.add_parser(
        name="export",
        help="export a snippet",
        description="Export a snippet."
    )
    
    export.register("type", "path", type_path)
    
    exclusive = export.add_mutually_exclusive_group(required=True)    
    exclusive.add_argument("-n", "--name", type=str, 
        help="the name of the snippet to export")
    exclusive.add_argument("-i", "--id", type=str,
        help="the ID of the snippet to export")
    
    export.add_argument("-p", "--path", type="path", default=Path.cwd(),
        help="the path where the snippet will be exported. Defaults to "
             "the current working directory.")
    export.add_argument("-f", "--force", action="store_true",
        help="force the snippet exportation")
    
    export.set_defaults(func=main)