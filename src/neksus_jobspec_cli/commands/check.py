"""Project check command."""

from __future__ import annotations

from typing import Annotated

import click
import typer
from rich.table import Table

from neksus_jobspec.app import ProjectUseCase
from neksus_jobspec_cli.commands.common import (
    handle_expected_error,
    print_error,
    print_json,
    print_success,
    print_warning,
    stdout,
)
from neksus_jobspec.errors import NeksusError

EXPECTED_COMMAND_ERRORS = (typer.BadParameter, click.UsageError, NeksusError, OSError, ValueError)
project_use_case = ProjectUseCase()


def app(
    strict: Annotated[bool, typer.Option("--strict", help="Treat warnings as failures.")] = False,
    format: Annotated[
        str,
        typer.Option("--format", help="Output format: human or github."),
    ] = "human",
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Run project-level checks."""
    try:
        if json and format == "github":
            raise typer.BadParameter(
                "--json and --format github are mutually exclusive.",
                param_hint="--format",
            )
        # Discover project root then execute all configured checks.
        payload = project_use_case.check(strict=strict).model_dump()
    except EXPECTED_COMMAND_ERRORS as exc:
        handle_expected_error(exc, as_json=json)
        return

    ok = bool(payload["ok"])

    # Keep JSON output stable for automation and tests.
    if json:
        print_json(payload)
        raise typer.Exit(0 if ok else 1)

    if format == "github":
        for error in payload["errors"]:
            typer.echo(f"::error file={error['path']}::{error['message']}")
        for warning in payload["warnings"]:
            typer.echo(f"::warning file={warning['path']}::{warning['message']}")
        raise typer.Exit(0 if ok else 1)
    if format != "human":
        raise typer.BadParameter(
            f"Unsupported format: {format}",
            param_hint="--format",
        )

    summary = Table(title="Project Checks")
    summary.add_column("Check", style="cyan")
    summary.add_column("Status", style="white")
    summary.add_column("Message", style="white")
    for check in payload["checks"]:
        summary.add_row(check["name"], "ok" if check["ok"] else "failed", check["message"])
    stdout.print(summary)

    if ok:
        print_success("Project check passed.")
        for warning in payload["warnings"]:
            print_warning(f"Warning [{warning['path']}] {warning['message']}")
        return

    print_error("Project check failed.")
    for check in payload["checks"]:
        if not check["ok"]:
            print_error(f"Check failed: {check['name']} - {check['message']}")
    for error in payload["errors"]:
        print_error(f"Error [{error['path']}] {error['message']}")
    for warning in payload["warnings"]:
        print_warning(f"Warning [{warning['path']}] {warning['message']}")
    raise typer.Exit(1)
