"""Project check command."""

from __future__ import annotations

from typing import Annotated

import typer

from neksus.cli.commands.common import handle_expected_error, print_json, stderr, stdout
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

    if result.ok:
        stdout.print("Project check passed.")
        if result.warnings:
            for warning in result.warnings:
                stdout.print(f"Warning [{warning.path}] {warning.message}")
        return

    stderr.print("Project check failed.")
    for check in result.checks:
        if not check.ok:
            stderr.print(f"Check failed: {check.name} - {check.message}")
    for error in result.errors:
        stderr.print(f"Error [{error.path}] {error.message}")
    for warning in result.warnings:
        stderr.print(f"Warning [{warning.path}] {warning.message}")
    raise typer.Exit(1)
