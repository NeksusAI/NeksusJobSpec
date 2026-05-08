"""Theme discovery and development commands."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import click
import typer

from neksus_jobspec.app.theme_dev_service import ThemeDevService
from neksus_jobspec.errors import NeksusError
from neksus_jobspec_cli.commands.common import (
    handle_expected_error,
    print_json,
    print_kv_table,
    print_success,
)

app = typer.Typer(help="Built-in and custom theme commands")
service = ThemeDevService()
EXPECTED_COMMAND_ERRORS = (typer.BadParameter, click.UsageError, NeksusError, OSError, ValueError)


@app.callback(invoke_without_command=True)
def themes_root(
    ctx: typer.Context,
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """List available themes."""
    if ctx.invoked_subcommand is not None:
        return
    themes = service.list_themes()
    if json:
        print_json({"ok": True, "themes": themes})
        return
    print_kv_table("Themes", [(item["name"], str(item["description"])) for item in themes])


@app.command("list")
def themes_list(
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """List available themes."""
    themes = service.list_themes()
    if json:
        print_json({"ok": True, "themes": themes})
        return
    print_kv_table("Themes", [(item["name"], str(item["description"])) for item in themes])


@app.command("show")
def themes_show(
    name: Annotated[str, typer.Argument(help="Theme name or custom theme directory path.")],
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Show metadata for a built-in theme or custom theme package."""
    try:
        theme = service.show_theme(name)
    except EXPECTED_COMMAND_ERRORS as exc:
        handle_expected_error(exc, as_json=json)
        return

    if json:
        print_json({"ok": True, "theme": theme})
        return

    print_kv_table(
        f"Theme: {theme['name']}",
        [
            ("Source", str(theme.get("source", "-"))),
            ("Version", str(theme.get("version") or "-")),
            ("Description", str(theme.get("description") or "-")),
            ("Templates", ", ".join(theme.get("templates", []))),
            ("Assets", ", ".join(theme.get("assets", []))),
        ],
    )


@app.command("validate")
def themes_validate(
    theme_path: Annotated[Path, typer.Argument(help="Path to a custom filesystem theme package.")],
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Validate a custom theme package and run a render smoke test."""
    try:
        payload = service.validate_theme_path(theme_path)
    except EXPECTED_COMMAND_ERRORS as exc:
        handle_expected_error(exc, as_json=json)
        return

    if json:
        print_json(payload)
        return
    print_success(f"Theme package is valid: {payload['path']}")


@app.command("init")
def themes_init(
    target: Annotated[Path, typer.Argument(help="Target directory to create theme scaffold in.")],
    force: Annotated[
        bool, typer.Option("--force", help="Allow writing into non-empty directory.")
    ] = False,
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Create a minimal custom theme package scaffold."""
    try:
        payload = service.init_theme(target, force=force)
    except EXPECTED_COMMAND_ERRORS as exc:
        handle_expected_error(exc, as_json=json)
        return

    if json:
        print_json(payload)
        return
    print_success(f"Initialized theme scaffold: {payload['path']}")
