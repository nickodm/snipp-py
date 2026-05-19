from shutil import rmtree

from . import *

def abort_edit(snippet: Snippet) -> int:
    if not is_locked(snippet):
        printerr("The snippet is not being edited.")
        return 1
    
    temp_dir = get_temp_dir(snippet)
    try:
        rmtree(temp_dir)
    except PermissionError:
        printerr("Error: The files are still open.")
        return 1

    unlock(snippet)
    
    print(":white_check_mark: Aborted.")
    return 0