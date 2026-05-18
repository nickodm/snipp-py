from pathlib import Path

from ..core import *



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
    if len(id) < 5:
        printerr("Error: The ID is too short.")
        return 1
    
    snippet = find_by(name, id)

    if snippet is None:
        printerr("Snippet not found.")
        return 1
    
    if snippet.creation_date:
        fdate: str = snippet.creation_date.strftime("%Y-%m-%d %H:%M")
    else:
        fdate: str = "[bright_black][Not registered]"
    
    print(f"[bold]NAME          :[/] {snippet.name}")
    print(f"[bold]ID            :[/] {snippet.uuid}")
    print(f"[bold]CREATION DATE :[/] {fdate}")
    print(f"[bold]GIT INIT?     :[/] {snippet.git_init}")
    print(f"[bold]DESCRIPTION   :[/] {snippet.description}")
    
    if tree:
        console.rule("[Tree]")
        print_tree(snippet)
    
    return 0