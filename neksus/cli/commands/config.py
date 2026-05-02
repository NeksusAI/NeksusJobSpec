"""Config commands."""

from __future__ import annotations

from typing import Annotated

import typer

from neksus.cli.commands.common import (
    handle_expected_error,
    print_json,
    print_kv_table,
    print_success,
    stdout,
)
from neksus.core.project.config import load_project_config, set_config_key
from neksus.core.project.discovery import find_project_root

app = typer.Typer(help="Project config commands")


@app.command("get")
def config_get(
    key: Annotated[str | None, typer.Argument(help="Optional config key to read.")] = None,
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Read config values."""
    try:
        # Config commands require project discovery first.
        root = find_project_root()
        config = load_project_config(root)
    except Exception as exc:  # noqa: BLE001
        handle_expected_error(exc, as_json=json)
        return

    data = config.model_dump()
    # Return either one key or full config payload.
    if key is not None:
        if key not in data:
            handle_expected_error(ValueError(f"Unknown config key: {key}"), as_json=json)
            return
        value = data[key]
        if json:
            print_json({"ok": True, "key": key, "value": value})
            return
        stdout.print(value)
        return

    if json:
        print_json({"ok": True, "config": data})
        return
    print_kv_table("Project Config", [(key, str(value)) for key, value in data.items()])


@app.command("set")
def config_set(
    key: Annotated[str, typer.Argument(help="Config key to update.")],
    value: Annotated[str, typer.Argument(help="New value for the key.")],
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Set mutable config keys."""
    try:
        # Validation and mutability checks happen in core layer.
        root = find_project_root()
        updated = set_config_key(root, key, value)
    except Exception as exc:  # noqa: BLE001
        handle_expected_error(exc, as_json=json)
        return

    if json:
        print_json({"ok": True, "config": updated.model_dump()})
        return
    print_success(f"Updated {key}.")
