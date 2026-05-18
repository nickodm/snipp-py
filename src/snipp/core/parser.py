"""
Module to generate the argument parser that runs the program.
"""

from argparse import ArgumentParser, _SubParsersAction
from pathlib import Path
from typing import Callable, TypeAlias, TYPE_CHECKING

from snipp import __version__

__all__ = ["command_register", "SubParser", "type_path"]

if TYPE_CHECKING:
    SubParser: TypeAlias = _SubParsersAction[ArgumentParser]
else:
    SubParser: TypeAlias = _SubParsersAction

_builders: list[Callable[[SubParser], None]] = []

def type_path(s: str) -> Path:
    """The path type. This expands user and becomes the path absolute.

    :param str s: The path as a string.
    :return Path: The absolute path.
    """
    return Path(s).expanduser().absolute()

def build() -> ArgumentParser:
    """Build the argument parser.

    :return ArgumentParser: The argument parser.
    """
    parser = ArgumentParser(
        prog="snipp",
        description="A simple program to manage file and directory snippets."
    )
    
    parser.register("type", "path", type_path)
    
    parser.add_argument("-v", "--version", action="version", version=__version__)
    
    cmds = parser.add_subparsers(
        title="subcommands",
        dest="command"
    )
    
    for builder in _builders:
        builder(cmds)
    
    return parser

def command_register(func: Callable[[SubParser], None]
    ) -> Callable[[SubParser], None]:
    """Decorator for functions that registers commands.

    :param Callable[[SubParser], None] func: The register function.
    :return Callable[[SubParser], None]: The register function.
    """
    _builders.append(func)
    return func