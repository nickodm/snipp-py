from shutil import rmtree
import logging

from . import *

logger = logging.getLogger(__name__)

def done_edit(snippet: Snippet) -> int:
    if not is_locked(snippet):
        printerr("The snippet is not being edited.")
        return 1
    
    temp_dir: Path = get_temp_dir(snippet)
    
    logging.info(f"Edit done {snippet}")
    with console.status("Saving changes..."):
        snippet.update_contents(temp_dir)
    
    logging.info(f"Deleting tempdir \"{temp_dir}\".")
    rmtree(temp_dir)
    unlock(snippet)
    print(":white_check_mark: Changes saved successfully.")
    return 0