from ..core import *
from ..core.parser import command_register, SubParser

def print_tree(snippet: Snippet) -> None:
    """Print the tree of the Snippet.

    :param Snippet snippet: The snippet to print the tree.
    """
    file_count = len(snippet.namelist())

    if file_count == 0:
        print("Snippet has no contents.")
        return
    
    print("[bold blue]" + snippet.name.upper())
    
    def get_indent(n: int) -> str:
        buff = ""
        
        for i in range(n):
            if i % 3 == 0:
                buff += "[dark_orange]|[/]"
            else:
                buff += " "
        
        return buff
    
    dir_count: int = 0
    last: tuple[str] = tuple()
    for path in snippet.namelist():
        branch = "[dark_orange]" + "|-" + "[/]"
        
        current: tuple[str] = path.parts
        indent = 0
        for index, part in enumerate(current):
            l = last[index] if len(last) > index else None
            is_dir = index < len(current) - 1
            
            if part != l:
                if is_dir:
                    part = "[blue]" + part + "[/]"
                    dir_count += 1
                
                print(get_indent(indent) + branch + " " + part, highlight=False)
            indent += 3
        
        last = current
    
    print(f"\nSnippet has {file_count} files and {dir_count} directories.")

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