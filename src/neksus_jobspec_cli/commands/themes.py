"""Theme discovery commands."""

from __future__ import annotations

from typing import Annotated

import click
import typer

from neksus_jobspec_cli.commands.common import handle_expected_error, print_json, print_kv_table
from neksus_jobspec.jobspec.rendering import get_theme_metadata, list_theme_metadata
from neksus_jobspec.errors import NeksusError

app = typer.Typer(help="Built-in render theme commands")
EXPECTED_COMMAND_ERRORS = (typer.BadParameter, click.UsageError, NeksusError, OSError, ValueError)


@app.callback(invoke_without_command=True)
def themes_root(
    ctx: typer.Context,
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """List built-in themes."""
    if ctx.invoked_subcommand is not None:
        return
    themes = [item.model_dump() for item in list_theme_metadata()]
    if json:
        print_json({"ok": True, "themes": themes})
        return
    print_kv_table("Built-in Themes", [(item["name"], item["description"]) for item in themes])


@app.command("show")
def themes_show(
    name: Annotated[str, typer.Argument(help="Theme name.")],
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Show one theme metadata record."""
    try:
        theme = get_theme_metadata(name).model_dump()
    except EXPECTED_COMMAND_ERRORS as exc:
        handle_expected_error(exc, as_json=json)
        return

    if json:
        print_json({"ok": True, "theme": theme})
        return

    print_kv_table(
        f"Theme: {theme['name']}",
        [
            ("Description", str(theme["description"])),
            ("Supported Formats", ", ".join(theme["supported_formats"])),
            ("CSS Embedded", "yes" if theme["css_embedded"] else "no"),
            ("Layout Notes", str(theme["layout_notes"])),
            ("Token Hints", ", ".join(theme["token_hints"])),
        ],
    )
