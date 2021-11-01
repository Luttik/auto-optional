from pathlib import Path
from typing import List

import typer

from auto_optional.file_handling import convert_path

app = typer.Typer()


@app.command()
def main(path: List[Path] = typer.Argument(None)) -> None:
    if not path:
        path = [Path(".")]
    converted_files = sum(convert_path(p) for p in path)
    if converted_files:
        typer.echo(f"{converted_files} were fixed.")
    else:
        typer.echo("No issues were found.")


if __name__ == "__main__":
    typer.run(main)
