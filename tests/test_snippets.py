from pathlib import Path, PurePath
import os
import pytest

os.environ["SNIPP_DEBUG"] = "1"

from snipp import core
from snipp.core.snippet import Snippet

files = [
    ["README.md", "# Dummy Dir\n\nMade for testing"],
]

for i in range(1, 7):
    files.append([
    f"assets/asset{i}.json",
    "{'name':'asset%i', 'type':'asset'}" % i
])
 

@pytest.fixture
def example_dir(tmp_path: Path) -> Path:
    root: Path = Path(tmp_path) / "dummy_dir"
    root.mkdir()
    
    for path, contents in files:
        path = root / path
        path.parent.mkdir(exist_ok=True, parents=True)
        
        if path.suffix != "":
            path.write_text(contents)
    
    return root

def test_init() -> None:
    assert core.DEBUG_MODE

def test_create(example_dir) -> None:
    namelist = [PurePath(path) for path, _ in files]
    
    snip: Snippet = Snippet.create(
        origin=example_dir,
        name="SNIPP TEST",
        description="SNIPP MADE JUST FOR TESTING",
        git_init=True
    )
    
    assert snip.name == "SNIPP TEST"
    assert snip.path \
        == core.paths.SNIPPETS / (snip.metadata.sanitized_name() + snip.SUFFIX)
    assert len(snip.id) == 36
    assert snip.creation_date is not None
    assert snip.description == "SNIPP MADE JUST FOR TESTING"
    assert snip.git_init == True
    assert snip.namelist() == namelist

def test_rename(example_dir) -> None:
    name = "SNIPP TEST"
    new_name = "SNIPP TEST RENAMED"
    
    snip: Snippet = Snippet.create(
        origin=example_dir,
        name=name,
        description="SNIPP MADE JUST FOR TESTING",
        git_init=True
    )

    snip.rename(new_name)
    path = snip.path
    
    assert snip.name == new_name
    assert path.exists()
    
    snip: Snippet = Snippet.load(path)
    
    assert snip.name == new_name