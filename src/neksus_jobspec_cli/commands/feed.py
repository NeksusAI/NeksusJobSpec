"""Feed and sitemap commands."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import click
import typer
from pydantic import ValidationError

from neksus_jobspec.errors import NeksusError
from neksus_jobspec.jobspec.feeds import (
    expand_input_paths,
    render_jobs_json_feed,
    render_jobs_xml_feed,
    render_sitemap,
)
from neksus_jobspec.jobspec.parser import load_jobspec
from neksus_jobspec_cli.commands.common import handle_expected_error, print_json, print_success

app = typer.Typer(help="Feed commands")
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
        paths = expand_input_paths(inputs)
        if not paths:
            raise typer.BadParameter("No input files found.")
        specs = []
        invalid: list[str] = []
        for path in paths:
            try:
                specs.append(load_jobspec(path))
            except Exception:
                invalid.append(str(path))
        if invalid and not skip_invalid:
            raise NeksusError(f"Invalid JobSpec input(s): {', '.join(invalid)}")
        if target == "jobs-json":
            content = render_jobs_json_feed(specs)
        elif target == "jobs-xml":
            content = render_jobs_xml_feed(specs)
        else:
            raise typer.BadParameter("Unsupported target. Use: jobs-json or jobs-xml")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    except EXPECTED_COMMAND_ERRORS as exc:
        handle_expected_error(exc, as_json=json)
        return

    payload = {
        "ok": True,
        "target": target,
        "output": str(out),
        "count": len(specs),
        "invalid": invalid,
    }
    if json:
        print_json(payload)
        return
    print_success(f"Exported {len(specs)} job(s) to {out} ({target})")


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
        paths = expand_input_paths(inputs)
        if not paths:
            raise typer.BadParameter("No input files found.")
        specs = [load_jobspec(path) for path in paths]
        content = render_sitemap(specs, base_url, exclude_closed=exclude_closed)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    except EXPECTED_COMMAND_ERRORS as exc:
        handle_expected_error(exc, as_json=json)
        return

    payload = {
        "ok": True,
        "output": str(out),
        "count": len(specs),
        "exclude_closed": exclude_closed,
    }
    if json:
        print_json(payload)
        return
    print_success(f"Generated sitemap for {len(specs)} job(s): {out}")
