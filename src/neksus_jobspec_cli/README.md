# neksus_jobspec_cli

Typer-based command-line package for Neksus JobSpec.

## Purpose

Expose user-facing CLI commands while keeping command modules thin.

## Structure

- `main.py`: command registration.
- `commands/`: grouped command modules.

## Rule

CLI modules should delegate orchestration to `neksus_jobspec.app` and avoid embedding business logic.
