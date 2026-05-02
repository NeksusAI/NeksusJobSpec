"""Project check command."""

from __future__ import annotations

from typing import Annotated

import typer
from rich.table import Table

from neksus.cli.commands.common import (
    handle_expected_error,
    print_error,
    print_json,
    print_success,
    print_warning,
    stdout,
)
from neksus.core.project.checks import run_project_checks
from neksus.core.project.discovery import find_project_root


def app(
    strict: Annotated[bool, typer.Option("--strict", help="Treat warnings as failures.")] = False,
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Run project-level checks."""
    try:
        # Discover project root then execute all configured checks.
        root = find_project_root()
        result = run_project_checks(root, strict=strict)
    except Exception as exc:  # noqa: BLE001
        handle_expected_error(exc, as_json=json)
        return

    payload = {
        "ok": result.ok,
        "checks": [check.model_dump() for check in result.checks],
        "errors": [error.model_dump() for error in result.errors],
        "warnings": [warning.model_dump() for warning in result.warnings],
    }

    # Keep JSON output stable for automation and tests.
    if json:
        print_json(payload)
        raise typer.Exit(0 if result.ok else 1)

    summary = Table(title="Project Checks")
    summary.add_column("Check", style="cyan")
    summary.add_column("Status", style="white")
    summary.add_column("Message", style="white")
    for check in result.checks:
        summary.add_row(check.name, "ok" if check.ok else "failed", check.message)
    stdout.print(summary)

    if result.ok:
        print_success("Project check passed.")
        if result.warnings:
            for warning in result.warnings:
                print_warning(f"Warning [{warning.path}] {warning.message}")
        return

    print_error("Project check failed.")
    for check in result.checks:
        if not check.ok:
            print_error(f"Check failed: {check.name} - {check.message}")
    for error in result.errors:
        print_error(f"Error [{error.path}] {error.message}")
    for warning in result.warnings:
        print_warning(f"Warning [{warning.path}] {warning.message}")
    raise typer.Exit(1)
