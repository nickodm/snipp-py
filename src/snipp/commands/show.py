from pathlib import Path

from ..core import *
from ..core.parser import command_register, SubParser

def print_tree(snippet: Snippet) -> None:
    last_parent: Path | None = None
    
    nl = snippet.namelist()
    
    if len(nl) == 0:
        print("Snippet has no contents.")
        return
    
    print(snippet.name)
    for i, path in enumerate(nl):
        branch: str = "|-" if i < len(nl) - 1 else "└─"
        
        if path.name.startswith("."):
            print(branch + path.name)
            continue
        
        if path.parents[0] != last_parent:
            last_parent = path.parents[0]
            print("|-" + last_parent.name)
        
        print(path)
        

def main(name: str | None, id: str | None, tree: bool) -> int:
    snippet = find_by(name, id)
    
    if snippet.creation_date:
        fdate: str = snippet.creation_date.strftime("%Y-%m-%d %H:%M")
    else:
        fdate: str = "[bright_black][Not registered]"
    
    print(f"[bold]NAME          :[/] {snippet.name}")
    print(f"[bold]ID            :[/] {snippet.id}")
    print(f"[bold]CREATION DATE :[/] {fdate}")
    print(f"[bold]GIT INIT?     :[/] {snippet.git_init}")
    print(f"[bold]DESCRIPTION   :[/] {snippet.description}")
    
    if tree:
        console.rule("[Tree]")
        print_tree(snippet)
    
    return 0

@command_register
def register(cmds: SubParser) -> None:
    show = cmds.add_parser(
        name="show",
        help="show information about a snippet",
        description="Show information about a specified snippet."
    )
    
    exclusive = show.add_mutually_exclusive_group(required=True)
    
    exclusive.add_argument("-n", "--name", type=str, 
        help="the name of the snippet to show")
    exclusive.add_argument("-i", "--id", type=str,
        help="the ID of the snippet to show")
    
    show.add_argument("--no-tree", action="store_false", dest="tree",
        help="don't show the snippet's directory tree")
    
    # show.add_argument("--toml", action="store_true",)
    show.set_defaults(func=main)