from pathlib import Path

from ..core import *
from ..core.parser import *

def main(path: Path, update: bool) -> int:
    if not path.exists():
        printerr("Error: The path doesn't exists.")
        return 1
    
    if path.is_dir():
        printerr("Error: The path is a dir.")
        return 1
    
    snippet = Snippet.load(path)
    
    if not update and already_stored(snippet):
        printerr("The snippet is already stored "
                 f"(id [blue]{snippet.uuid[:5]}[/blue]).")
        return 1
    
    snippet.path = snippet.assigned_path()
    with console.status("Importing..."):
        with open(path, "rb") as fp:
            read = fp.read()
        
        with open(snippet.path, "wb") as fp:
            fp.write(read)
    
    print(f":white_check_mark: Imported snippet \"{snippet.name}\".")
    return 0

@command_register
def register(cmds: SubParser) -> None:
    import_cmd = cmds.add_parser(
        name="import",
        help="import a snippet",
        description="Import a snippet."
    )
    
    import_cmd.register("type", "path", type_path)
    
    import_cmd.add_argument("path", type="path",
        help="the path where the snippet to import is saved")
    import_cmd.add_argument("-u", "--update", action="store_true",
        help="if the snippet is already stored, update it")
    
    import_cmd.set_defaults(func=main)