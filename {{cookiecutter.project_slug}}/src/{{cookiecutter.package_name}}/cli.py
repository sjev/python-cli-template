from __future__ import annotations

from typing import Annotated

import typer

app = typer.Typer(no_args_is_help=True)


def _version_callback(value: bool) -> None:
    if value:
        from importlib.metadata import version

        print(version("{{ cookiecutter.project_slug }}"))
        raise typer.Exit()


@app.callback()
def main(
    _version: Annotated[
        bool,
        typer.Option("--version", "-v", help="Show version and exit.", callback=_version_callback),
    ] = False,
) -> None:
    """{{ cookiecutter.description }}"""


@app.command()
def hello(name: str = "world") -> None:
    """Say hello."""
    print(f"Hello, {name}!")
