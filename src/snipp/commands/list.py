"""
list [--oneline]
"""
from ..core import * 
from ..core.parser import command_register, SubParser

def print_normal():
    key_format: str = "bold"
    counter = 0
    for snippet in load_snippets():
        if snippet.creation_date:
            date = snippet.creation_date.strftime("%Y-%m-%d %H:%H")
        else:
            date = None
        
        console.rule(f"[{counter:0>2}]", align="left")
        print(f"[{key_format}]NAME          :[/] {snippet.name}")
        print(f"[{key_format}]ID            :[/] {snippet.id}")
        print(f"[{key_format}]CREATION DATE :[/] {date}")
        print(f"[{key_format}]GIT INIT?     :[/] {snippet.git_init}",
              highlight=False)
        print(f"[{key_format}]DESCRIPTION   :[/] {snippet.description}")
        counter += 1
    
    if counter > 0:
        console.rule()
    
    print(f"There are {counter} saved snippets.")

def print_oneline():
    for snippet in load_snippets():
        print(f"[[bold yellow]{snippet.min_id}[/]] {snippet.name}")

def main(oneline: bool) -> int:
    with console.pager(styles=True):
        if oneline:
            print_oneline()
        else:
            print_normal()
    
    return 0

@command_register
def register(cmds: SubParser) -> None:
    list = cmds.add_parser(
        name="list",
        help="list all the saved snippets",
        description="List all the saved snippets."
    )
    list.add_argument(
        "--oneline",
        action="store_true",
        help="list just oneline for each snippet"
    )
    list.set_defaults(func=main)