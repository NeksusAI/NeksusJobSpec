"""Feed and sitemap commands."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import click
import typer
from pydantic import ValidationError

from neksus_jobspec.app import FeedUseCase
from neksus_jobspec.errors import NeksusError
from neksus_jobspec_cli.commands.common import handle_expected_error, print_json, print_success

app = typer.Typer(help="Feed commands")
feed_use_case = FeedUseCase()
EXPECTED_COMMAND_ERRORS = (
    typer.BadParameter,
    click.UsageError,
    NeksusError,
    OSError,
    ValidationError,
    ValueError,
)


@app.command("export")
def feed_export(
    inputs: Annotated[list[str], typer.Argument(help="Input files, globs, or directories.")],
    target: Annotated[str, typer.Option("--target", help="jobs-json or jobs-xml.")],
    out: Annotated[Path, typer.Option("--out", help="Output file path.")],
    skip_invalid: Annotated[
        bool, typer.Option("--skip-invalid", help="Skip invalid inputs.")
    ] = False,
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Export multiple JobSpecs into a feed format."""
    try:
        if target not in {"jobs-json", "jobs-xml"}:
            raise typer.BadParameter("Unsupported target. Use: jobs-json or jobs-xml")
        payload = feed_use_case.export(
            inputs=inputs,
            target=target,
            out=out,
            skip_invalid=skip_invalid,
        )
    except EXPECTED_COMMAND_ERRORS as exc:
        handle_expected_error(exc, as_json=json)
        return

    if json:
        print_json(payload)
        return
    print_success(f"Exported {payload['count']} job(s) to {out} ({target})")


@app.command("sitemap")
def feed_sitemap(
    inputs: Annotated[list[str], typer.Argument(help="Input files, globs, or directories.")],
    base_url: Annotated[str, typer.Option("--base-url", help="Base public jobs URL.")],
    out: Annotated[Path, typer.Option("--out", help="Output sitemap path.")],
    exclude_closed: Annotated[
        bool, typer.Option("--exclude-closed", help="Exclude closed/expired campaigns.")
    ] = False,
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Generate sitemap.xml from multiple JobSpecs."""
    try:
        payload = feed_use_case.sitemap(
            inputs=inputs,
            base_url=base_url,
            out=out,
            exclude_closed=exclude_closed,
        )
    except EXPECTED_COMMAND_ERRORS as exc:
        handle_expected_error(exc, as_json=json)
        return

    if json:
        print_json(payload)
        return
    print_success(f"Generated sitemap for {payload['count']} job(s): {out}")
