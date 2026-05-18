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

from .core import *
from .core import parser
from .core.paths import init_project_dir
from . import __version__

from . import commands # DO NOT DELETE! This loads the commands.

def main() -> int:
    argparser = parser.build()
    args = argparser.parse_args()
    
    func = args.func
    del args.command, args.func
    
    init_project_dir()
    return func(**vars(args))

def run() -> int:
    try:
        return main()
    except KeyboardInterrupt:
        printerr("Process killed by user.")
        return 1
    except SnippError as e:
        printerr(f"Error: {e}")
        return e.exit_code
    except Exception:
        err.print_exception()
        return 1

if __name__ == "__main__":
    exit(run())