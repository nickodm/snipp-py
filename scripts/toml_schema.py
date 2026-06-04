"""
Script to compile JSON schemas written in TOML to fast json schema.

Run:
```bash
poetry run python scripts/toml_schema.py
```
"""

from pathlib import Path
from argparse import ArgumentParser
import fastjsonschema
import tomlkit
import sys

__version__ = "v0.1.0"
__version_info__ = (0, 1, 0)

def compile(source: Path, output: Path) -> None:
    """Compile a TOML file to a fast json schema compiled Python code.

    :param Path source: The path of the TOML file.
    :param Path output: The path to dump the compiled schema.
    """
    with open(source, "r") as fp:
        data: str = fp.read()
    
    schema = tomlkit.parse(data) # dict-like
    code: str = fastjsonschema.compile_to_code(schema)
    
    with open(output, "w") as fp:
        fp.write(code)

def parser() -> ArgumentParser:
    def path_type(s: str) -> Path:
        return Path(s).expanduser().absolute()

    parser = ArgumentParser(
        prog="toml_schema",
        description="Compile a JSON schema written in TOML."        
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=__version__
    )
    
    parser.add_argument(
        "file",
        help="the schema to compile",
        type=path_type
    )
    
    parser.add_argument(
        "-o", "--output",
        help="specify the output path",
        metavar="PATH",
        type=path_type
    )
    
    parser.add_argument(
        "-f", "--force",
        help="force the compilation, even if the output already exists",
        action="store_true"
    )
    
    return parser

def main() -> int:
    args = parser().parse_args()
    
    file: Path = args.file
    output: Path = args.output
    force: bool = args.force
    
    if output is None:
        output: Path = file.with_suffix(".py")

    if not force and output.exists():
        print("Error: The output already exists.", file=sys.stderr)
        return 1
    
    if not file.exists():
        print("Error: The file doesn't exists.", file=sys.stderr)
        return 1
    
    compile(file, output)
    print(f"Compiled \"{file.name}\".")
    return 0

if __name__ == "__main__":
    exit(main())