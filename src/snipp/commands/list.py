
from ..core import *

def print_normal():
    counter = 0
    for snippet in load_snippets():
        console.rule(f"[{counter:0>2}]", align="left")
        print(f"[bold]NAME          :[/] {snippet.name}")
        print(f"[bold]ID            :[/] {snippet.uuid}")
        print(f"[bold]CREATION DATE :[/] {snippet.creation_date}")
        print(f"[bold]GIT INIT?     :[/] {snippet.git_init}")
        print(f"[bold]DESCRIPTION   :[/] {snippet.description}")
        counter += 1
    
    if counter > 0:
        console.rule()
    
    print(f"There are {counter} saved snippets.")

def print_oneline():
    for snippet in load_snippets():
        print(f"[[bold blue]{snippet.uuid[:5]}[/]] {snippet.name}")

def main(oneline: bool) -> int:
    if oneline:
        print_oneline()
    else:
        print_normal()
    
    return 0