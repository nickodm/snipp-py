"""
snipp
|- list     List all the snippets.
|- create   Create a new snippet.
|- delete   Delete a snippet.
|- edit     Edit a snippet.
|- deploy   Deploy a snippet.
|- rename   Rename a snippet.
|- export   Export a snippet.
|- import   Import a snippet.
|- config   General configurations.
|- show     Show information about a snippet (structure, options, etc)
|- options  Manager snippet options.
    |- 
"""

from argparse import ArgumentParser
from pathlib import Path

from .core import *
from . import commands, __version__

def init_parser() -> ArgumentParser:
    def path(s: str) -> Path:
        return Path(s).expanduser().absolute()
    
    parser = ArgumentParser(
        prog="Snippets",
        description="A simple program to manage file and directory snippets."
    )
    
    parser.add_argument("-v", "--version", action="version", version=__version__)
    
    cmds = parser.add_subparsers(
        title="subcommands",
        dest="command"
    )
    
    create = cmds.add_parser(
        name="create",
        help="create a snippet from a directory",
        description="Create a snippet from a directory.")
    create.add_argument("name", type=str)

    exclusive = create.add_mutually_exclusive_group()
    exclusive.add_argument("-d", "--description", type=str, default='',
        help="add a description to the snippet")
    exclusive.add_argument("-D", "--description-file", type=path, dest="description_file",
        help="read the description from a file", metavar="PATH")
    
    create.add_argument("-p", "--path", type=path, default=Path.cwd(),
        help="the path where the snippet is (defaults to current working directory)")
    create.add_argument("--no-git", action="store_false", dest="git",
        help="don't init a git repository when using the use command")
    create.add_argument("--save-to", type=path, dest="to", metavar="PATH",
        help="specify a different path to save the snippet")
    
    create.set_defaults(func=commands.create)
    
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
    list.set_defaults(func=commands.list)
    
    show = cmds.add_parser(
        name="show",
        help="show information about a snippet",
        description="Show information about a specified snippet."
    )
    
    show.add_argument("id", type=str,
        help="the id of the snippet to show (minimum 5 chars)")
    show.add_argument("--no-tree", action="store_false", dest="tree",
        help="don't show the snippet's directory tree")
    
    # show.add_argument("--toml", action="store_true",)
    show.set_defaults(func=commands.show)
    
    delete = cmds.add_parser(
        name="delete",
        help="delete a snippet",
        description="Delete a saved snippet."
    )
    
    delete.add_argument("id", type=str, help="the snippet's id")
    
    delete.set_defaults(func=commands.delete)
    
    deploy = cmds.add_parser(
        name="deploy",
        help="deploy a snippet",
        description="Deploy a snippet."
    )
    
    exclusive = deploy.add_mutually_exclusive_group(required=True)
    
    exclusive.add_argument("-n", "--name", type=str, 
        help="the name of the snippet to deploy")
    exclusive.add_argument("-i", "--id", type=str,
        help="the ID of the snippet to deploy")
    
    deploy.add_argument("-p", "--path", type=path, default=Path.cwd(),
        help="the path where the snippet will be deployed. Defaults to "
             "the current working directory.")
    deploy.add_argument("-f", "--force", action="store_true",
        help="force the snippet creation")
    
    deploy.set_defaults(func=commands.deploy)
    
    export = cmds.add_parser(
        name="export",
        help="export a snippet",
        description="Export a snippet."
    )
    
    exclusive = export.add_mutually_exclusive_group(required=True)    
    exclusive.add_argument("-n", "--name", type=str, 
        help="the name of the snippet to export")
    exclusive.add_argument("-i", "--id", type=str,
        help="the ID of the snippet to export")
    
    export.add_argument("-p", "--path", type=path, default=Path.cwd(),
        help="the path where the snippet will be exported. Defaults to "
             "the current working directory.")
    export.add_argument("-f", "--force", action="store_true",
        help="force the snippet exportation")
    
    export.set_defaults(func=commands.export)
    
    import_cmd = cmds.add_parser(
        name="import",
        help="import a snippet",
        description="Import a snippet."
    )
    
    import_cmd.add_argument("path", type=path,
        help="the path where the snippet to import is saved")
    import_cmd.add_argument("-u", "--update", action="store_true",
        help="if the snippet is already stored, update it")
    
    import_cmd.set_defaults(func=commands.import_snipp)
    
    rename = cmds.add_parser(
        name="rename",
        help="change a snippet's name",
        description="Change a snippet's name."
    )
    
    exclusive = rename.add_mutually_exclusive_group(required=True)
    
    exclusive.add_argument("-n", "--name", type=str, 
        help="the name of the snippet to rename")
    exclusive.add_argument("-i", "--id", type=str,
        help="the ID of the snippet to rename")
    
    rename.add_argument("new_name",
        help="the new name for the snippet")
    
    rename.set_defaults(func=commands.rename)
    
    return parser

def main() -> int:
    parser = init_parser()
    args = parser.parse_args()
    
    func = args.func
    del args.command, args.func
    
    return func(**vars(args))

def run() -> int:
    try:
        return main()
    except KeyboardInterrupt:
        printerr("Process killed by user.")
        return 1
    except Exception:
        err.print_exception()
        return 1

if __name__ == "__main__":
    exit(run())