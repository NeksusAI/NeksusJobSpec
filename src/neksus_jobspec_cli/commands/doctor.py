"""Environment diagnostics command."""

from __future__ import annotations

from typing import Annotated

import typer

from neksus_jobspec.app.doctor_service import DoctorService
from neksus_jobspec_cli.commands.common import print_json, print_kv_table


def doctor_command(
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Run local environment and repository health checks."""
    payload = DoctorService().run()
    if json:
        print_json(payload)
        raise typer.Exit(0 if payload["ok"] else 1)

    rows = [(check["name"], f"{check['status']}: {check['detail']}") for check in payload["checks"]]
    print_kv_table("Neksus JobSpec Doctor", rows)
    raise typer.Exit(0 if payload["ok"] else 1)
