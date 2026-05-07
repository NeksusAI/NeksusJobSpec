"""Batch project render command."""

from __future__ import annotations

from typing import Annotated

import click
import typer
from pydantic import ValidationError

from neksus_jobspec.app import RenderUseCase
from neksus_jobspec_cli.commands.common import (
    handle_expected_error,
    print_error,
    print_json,
    print_success,
)
from neksus_jobspec.errors import NeksusError

EXPECTED_COMMAND_ERRORS = (
    typer.BadParameter,
    click.UsageError,
    NeksusError,
    OSError,
    ValidationError,
    ValueError,
)

render_use_case = RenderUseCase()


def render_command(
    all_specs: Annotated[
        bool,
        typer.Option("--all", help="No-op alias kept for command clarity."),
    ] = False,
    format: Annotated[str | None, typer.Option("--format", help="Render format.")] = None,
    theme: Annotated[str | None, typer.Option("--theme", help="Built-in render theme.")] = None,
    asset_base_url: Annotated[
        str | None,
        typer.Option(
            "--asset-base-url",
            help="Prefix relative component asset URLs in web output (e.g. ../assets).",
        ),
    ] = None,
    profile: Annotated[str | None, typer.Option("--profile", help="Render profile name.")] = None,
    clean: Annotated[
        bool,
        typer.Option("--clean", help="Remove output directory before render."),
    ] = False,
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Render all project JobSpecs into configured output directory."""
    _ = all_specs
    try:
        result = render_use_case.render_project(
            format=format,
            theme=theme,
            asset_base_url=asset_base_url,
            profile=profile,
            clean=clean,
        )
        payload = result.model_dump()
        if json:
            print_json(payload)
            raise typer.Exit(0 if result.ok else 1)

        if result.ok:
            print_success(f"Rendered {len(result.rendered)} JobSpec files")
            return
        print_error("Batch render failed: one or more JobSpec files are invalid.")
        raise typer.Exit(1)
    except typer.Exit:
        raise
    except EXPECTED_COMMAND_ERRORS as exc:
        handle_expected_error(exc, as_json=json)
