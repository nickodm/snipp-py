from rich.prompt import Confirm
import os

from ..core import *
from ..core.parser import *

def remove(snippet: Snippet) -> None:
    try:
        os.remove(snippet.path)
    except PermissionError:
        printerr(f":cross_mark: Cannot remove \"{snippet}\": "
                 "The file is being used or the process has no permission to "
                 "delete it.")

def main(force: bool) -> int:
    counter = 0
    for snippet in load_snippets():
        name = snippet.name
        id = snippet.min_id

        if force:
            remove(snippet)
            print(f"Deleted snippet \"[blue]{name}[/]\" ([yellow]{id}[/]).")
            counter += 1
            continue
        
        answer: bool = Confirm.ask(f"Delete snippet \"[blue]{name}[/]\" "
                             f"([yellow]{id}[/])?")
        
        if answer:
            remove(snippet)
            print(":white_check_mark: [red]Deleted.")
            counter += 1
        else:
            print(":cross_mark: [green]Not deleted.")
    
    print(f"Removed {counter} snippets.")
    return 0

@command_register
def register(cmds: SubParser) -> None:
    cmd = cmds.add_parser(
        name="purge",
        help="delete all the saved snippets",
        description="Delete all the saved snippets."
    )
    
    cmd.add_argument("-f", "--force", action="store_true",
        help="don't ask for confirmation for each snippet")
    
    cmd.set_defaults(func=main)