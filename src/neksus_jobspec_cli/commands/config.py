"""Config commands."""

from __future__ import annotations

from typing import Annotated

import click
import typer

from neksus_jobspec.app import ProjectUseCase
from neksus_jobspec_cli.commands.common import (
    handle_expected_error,
    print_json,
    print_kv_table,
    print_success,
    stdout,
)
from neksus_jobspec.errors import NeksusError

app = typer.Typer(help="Project config commands")
EXPECTED_COMMAND_ERRORS = (typer.BadParameter, click.UsageError, NeksusError, OSError, ValueError)
project_use_case = ProjectUseCase()


@app.command("get")
def config_get(
    key: Annotated[str | None, typer.Argument(help="Optional config key to read.")] = None,
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Read config values."""
    try:
        payload = project_use_case.config_get(key).model_dump(exclude_none=True)
    except EXPECTED_COMMAND_ERRORS as exc:
        handle_expected_error(exc, as_json=json)
        return

    if key is not None:
        value = payload["value"]
        if json:
            print_json({"ok": True, "key": key, "value": value})
            return
        stdout.print(value)
        return

    if json:
        print_json(payload)
        return
    data = payload["config"]
    print_kv_table("Project Config", [(key, str(value)) for key, value in data.items()])


@app.command("set")
def config_set(
    key: Annotated[str, typer.Argument(help="Config key to update.")],
    value: Annotated[str, typer.Argument(help="New value for the key.")],
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Set mutable config keys."""
    try:
        payload = project_use_case.config_set(key, value).model_dump()
    except EXPECTED_COMMAND_ERRORS as exc:
        handle_expected_error(exc, as_json=json)
        return

    if json:
        print_json(payload)
        return
    print_success(f"Updated {key}.")
