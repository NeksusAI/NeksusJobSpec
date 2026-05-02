"""Shared CLI helpers.

Centralizes output and consistent exit-code handling for all commands.
"""

from __future__ import annotations

import typer
from rich.console import Console

from neksus.core.errors import ConfigError, FileSystemError, NeksusError
from neksus.core.output import to_json

stdout = Console()
stderr = Console(stderr=True)


def print_json(payload: dict) -> None:
    """Print JSON payload to stdout."""
    stdout.print(to_json(payload))


def fail_json(message: str, code: int) -> None:
    """Emit standardized JSON error and exit."""
    print_json({"ok": False, "error": message, "code": code})
    raise typer.Exit(code)


def handle_expected_error(exc: Exception, as_json: bool = False) -> None:
    """Map known exceptions to stable exit codes and render output.

    Args:
        exc: Raised exception to map.
        as_json: If True, emit JSON error payload.
    """
    # Map domain exceptions to documented exit codes.
    if isinstance(exc, FileSystemError):
        code = 3
    elif isinstance(exc, ConfigError):
        code = 4
    elif isinstance(exc, NeksusError):
        code = 1
    else:
        code = 5

    # Keep error rendering consistent between human and JSON modes.
    if as_json:
        fail_json(str(exc), code)
    stderr.print(str(exc))
    raise typer.Exit(code)
