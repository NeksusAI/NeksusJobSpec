"""CLI entrypoint.

Defines the root Typer app and registers command groups.
"""

from __future__ import annotations

import typer

from neksus_jobspec_cli.commands.check import app as check_app
from neksus_jobspec_cli.commands.config import app as config_app
from neksus_jobspec_cli.commands.init import init_command
from neksus_jobspec_cli.commands.render import render_command
from neksus_jobspec_cli.commands.spec import app as spec_app
from neksus_jobspec_cli.commands.themes import app as themes_app
from neksus_jobspec_cli.commands.version import version_command

app = typer.Typer(help="Neksus JobSpec CLI")

# Top-level command registration.
app.command("version")(version_command)
app.command("init")(init_command)
app.add_typer(spec_app, name="spec")
app.command("render")(render_command)
app.command("check")(check_app)
app.add_typer(config_app, name="config")
app.add_typer(themes_app, name="themes")


if __name__ == "__main__":
    app()
