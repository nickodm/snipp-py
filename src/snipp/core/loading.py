from typing import Generator
from pathvalidate import sanitize_filename
import logging as _logging

from . import Snippet
from .errors import *
from .paths import SNIPPETS

logger = _logging.getLogger(__name__)

def load_snippets() -> Generator[Snippet, None, None]:
    """
    Load the saved snippets.

    :yield Snippet: Each found snippet.
    """
    if not SNIPPETS.exists():
        logger.error("snippet directory doesn't exists.")
        return
    
    for entry in SNIPPETS.iterdir():
        try:
            yield Snippet.load(entry)
        except InvalidSnippetError:
            pass

def find_by_id(id: str) -> Snippet:
    """Find and load a snippet by its ID.

    :param str id: The snippet's ID.
    :return Snippet: The found snippet.
    :raises IDTooShortError: When the ID is too short.
    :raise SnippetNotFoundError: When the snippet was not found.
    """
    if len(id) < Snippet.ID_MIN_LEN:
        logger.critical("ID too short: %s", id)
        raise IDTooShortError(id)
    
    if not SNIPPETS.exists():
        logger.critical("snippets directory doesn't exists.")
        raise SnippetNotFoundError()
    
    for file in SNIPPETS.iterdir():
        if not file.is_file():
            continue
        
        try:
            temp = Snippet.load(file)
            if temp.id.startswith(id):
                return temp
        except InvalidSnippetError:
            pass # We don't want this problems here
    
    return None

def find_by_name(name: str) -> Snippet:
    """Find and load a snippet by its name.

    :param str name: The snippet's name.
    :return Snippet: The found snippet.
    :raises SnippetNotFoundError: When the snippet was not found.
    """
    if not SNIPPETS.exists():
        logger.critical("snippets directory doesn't exists.")
        raise SnippetNotFoundError()
    
    name = sanitize_filename(name)
    path = SNIPPETS / (name + Snippet.SUFFIX)
    
    if not path.exists():
        raise SnippetNotFoundError()
    
    return Snippet.load(path)

def find_by(name: str | None = None, id: str | None = None) -> Snippet:
    """Find and load a snippet by its name or ID.

    :param str | None name: The snippet's name, defaults to None
    :param str | None id: The snippet's id, defaults to None
    :raises SnippetNotFoundError: When the snippet was not found.
    :raises IDTooShortError: When the ID is too short.
    :return Snippet: The found snippet.
    """
    if id is not None:
        snippet = find_by_id(id)
    else:
        snippet = find_by_name(name)

    if snippet is None:
        raise SnippetNotFoundError()
    
    return snippet