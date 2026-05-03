"""Init command."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from neksus.cli.commands.common import handle_expected_error, print_json, print_success
from neksus.core.project.init_project import init_project


def init_command(
    empty: Annotated[
        bool, typer.Option("--empty", help="Create project without an example JobSpec.")
    ] = False,
    force: Annotated[
        bool, typer.Option("--force", help="Overwrite existing project config/example files.")
    ] = False,
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Initialize a Neksus project in the current directory."""
    try:
        # Initialize from current working directory.
        created = init_project(Path.cwd(), empty=empty, force=force)
    except Exception as exc:  # noqa: BLE001
        handle_expected_error(exc, as_json=json)
        return

    # Emit either machine-readable or human-readable success output.
    if json:
        print_json({"ok": True, "created": created})
        return
    print_success("Initialized Neksus project.")
