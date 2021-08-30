from pathlib import Path

from auto_optional.convert import convert_path
import typer


def main(path: str = ".") -> None:
    converted_files = convert_path(Path(path))
    typer.echo(f"🚀 {converted_files} were fixed.")

typer.run(main)
