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
from logging.handlers import RotatingFileHandler
import logging as _logging

from .core import *
from .core import parser
from .core.paths import init_project_dir
from . import __version__

from . import commands # DO NOT DELETE! This loads the commands.

def init_logger() -> _logging.Logger:
    logger = _logging.getLogger()
    
    formatter = _logging.Formatter(
        fmt="%(levelname)s %(asctime)s - %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    handler = RotatingFileHandler(
        filename=paths.lastlog_path,
        maxBytes=1024**2*5,
        backupCount=1,
        encoding="utf-8"
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(_logging.INFO)
    return logger

logger = init_logger()

def main() -> int:
    argparser = parser.build()
    args = argparser.parse_args()
    
    func = args.func
    del args.command, args.func
    
    logger.info(f"Running snipp {__version__}.")
    init_project_dir()
    return func(**vars(args))

def run() -> int:
    try:
        return main()
    except KeyboardInterrupt:
        printerr("Process killed by user.")
        logger.critical("KeyboardInterrupt.")
        return 1
    except SnippError as e:
        printerr(f"Error: {e}")
        logger.critical(f"{e.__class__.__name__}: {e}", exc_info=True)
        return e.exit_code
    except Exception as e:
        printerr(f"An unexpected error has ocurred: {e}")
        print(f"Log file at [blue][{paths.lastlog_path}]")
        print("Please, report the error at "
              "https://github.com/nickodm/snipp-py/issues")
        logger.critical("Unexpected error", exc_info=True)
        return 1
    finally:
        logger.info("Shutting down...")
        _logging.shutdown()

if __name__ == "__main__":
    exit(run())