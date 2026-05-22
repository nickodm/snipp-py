import logging

from ...core import *
from ...core.parser import *

from .abort import abort_edit
from .done import done_edit
from . import *

logger = logging.getLogger(__name__)

def create_edit(snippet: Snippet) -> int:
    temp_dir = get_temp_dir(snippet)
    
    if is_locked(snippet):
        printerr("The snippet is already being edited in "
                 f"[blue][{temp_dir}][/].")
        return 1
    
    logger.info(f"Editing snippet {snippet}.")
    with console.status("Extracting snippet to a temporary directory..."):
        snippet.extract(temp_dir)
        lock(snippet)
    
    open_in_editor(temp_dir)
    print(f"Snippet extracted to: [blue][{temp_dir}][/]. "
          "Use \"snipp edit done\" when you finished your changes.")
    return 0

def main(name: str | None, id: str | None, subcmd: str | None) -> int:
    if (name or id) and subcmd is not None:
        printerr("You can't specify a subcommand when you start editing.")
        return 1
    
    snippet = find_locked()
    
    if subcmd is None:
        if snippet is None:
            snippet = find_by(name, id)
            return create_edit(snippet)
        else:
            printerr("Error: Another snippet is already being edited "
                     f"([blue]{snippet.name}[/], "
                     f"[yellow]{snippet.min_id}[/])")
            return 1
    
    if snippet is None:
        printerr("Error: No snippet is currently being edited.")
        return 1
    
    match subcmd:
        case "abort":
            return abort_edit(snippet)
        
        case "done":
            return done_edit(snippet)
        
        case _:
            # In theory, this should never happen
            raise NotImplementedError

@command_register
def register(cmds: SubParser) -> None:
    edit = cmds.add_parser(
        name="edit",
        help="edit a snippet",
        description="Edit a snippet."
    )
    
    exclusive = edit.add_mutually_exclusive_group()
    
    exclusive.add_argument("-n", "--name", type=str, 
        help="the name of the snippet to edit")
    exclusive.add_argument("-i", "--id", type=str,
        help="the ID of the snippet to edit")
    
    sub_cmds = edit.add_subparsers(
        title="subcommands",
        dest="subcmd"
        )
    
    done = sub_cmds.add_parser(
        name="done",
        help="finish editing a snippet and save changes",
        description="Finish the edition and save changes."
    )
    
    abort = sub_cmds.add_parser(
        name="abort",
        help="abort the edition, don't save changes",
        description="Abort the edition and don't save changes."
    )
    
    edit.set_defaults(func=main)