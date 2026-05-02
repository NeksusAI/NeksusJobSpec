"""Version command."""

from __future__ import annotations

from typing import Annotated

import typer

from neksus import __version__
from neksus.cli.commands.common import print_json, print_success


def version_command(
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Print CLI version."""
    # Keep version payload small and stable for scripts.
    if json:
        print_json({"name": "neksus", "version": __version__})
        return
    print_success(f"neksus {__version__}")
