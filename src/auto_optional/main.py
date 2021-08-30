from pathlib import Path

import typer

from auto_optional.convert import convert_path

app = typer.Typer()


@app.command()
def main(path: Path = typer.Argument(".")) -> None:
    converted_files = convert_path(path)
    if converted_files:
        typer.echo(f"{converted_files} were fixed.")
    else:
        typer.echo("No issues were found.")


if __name__ == "__main__":
    typer.run(main)
