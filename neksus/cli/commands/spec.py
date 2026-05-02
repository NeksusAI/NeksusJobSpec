"""Spec commands.

This module exposes create/validate/render/inspect operations for JobSpecs.
The command layer stays thin and delegates business logic to `neksus.core`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError

from neksus.cli.commands.common import (
    handle_expected_error,
    print_error,
    print_json,
    print_kv_table,
    print_success,
    print_warning,
    stdout,
)
from neksus.core.errors import ConfigError, FileSystemError
from neksus.core.jobspec.inspect import inspect_jobspec
from neksus.core.jobspec.models import JobSpec
from neksus.core.jobspec.parser import load_jobspec, load_yaml_file
from neksus.core.jobspec.renderer import render_jobspec
from neksus.core.jobspec.schema import jobspec_json_schema
from neksus.core.jobspec.templates import build_jobspec_template, dump_jobspec_yaml, slugify_name
from neksus.core.jobspec.validator import (
    pydantic_errors_to_issues,
    validate_spec_data,
    validate_spec_model,
)
from neksus.core.output import to_json
from neksus.core.project.config import load_project_config
from neksus.core.project.discovery import find_project_root

app = typer.Typer(help="JobSpec commands")


def _resolve_new_path(name: str, output: Path | None) -> Path:
    """Resolve output path for `spec new`.

    Priority:
    1) Explicit --output path
    2) Project config `spec_directory` if in a project
    3) Current working directory outside a project
    """
    slug = slugify_name(name)
    if not slug:
        raise FileSystemError("Name produces an empty slug.")
    if output:
        return output
    try:
        root = find_project_root()
        config = load_project_config(root)
        return root / config.spec_directory / f"{slug}.jobspec.yaml"
    except ConfigError:
        return Path.cwd() / f"{slug}.jobspec.yaml"


@app.command("new")
def spec_new(
    name: Annotated[str, typer.Argument(help="Name used to generate JobSpec id and file name.")],
    output: Annotated[Path | None, typer.Option("--output", help="Custom output path.")] = None,
    force: Annotated[bool, typer.Option("--force", help="Overwrite existing file.")] = False,
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Create a new JobSpec file."""
    try:
        # Resolve and guard output path before writing.
        target = _resolve_new_path(name, output)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not force:
            raise FileSystemError(f"File already exists: {target}. Use --force to overwrite.")

        # Generate valid template and validate once before writing to disk.
        template = build_jobspec_template(name)
        JobSpec.model_validate(template)
        target.write_text(dump_jobspec_yaml(template), encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        handle_expected_error(exc, as_json=json)
        return

    if json:
        print_json({"ok": True, "file": str(target)})
        return
    print_success(f"Created JobSpec: {target}")


@app.command("validate")
def spec_validate(
    path: Annotated[Path, typer.Argument(help="Path to a JobSpec YAML file.")],
    strict: Annotated[bool, typer.Option("--strict", help="Treat warnings as failures.")] = False,
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Validate a JobSpec file."""
    try:
        # Parse and validate raw YAML file into structured result.
        data = load_yaml_file(path)
        result = validate_spec_data(data)
    except Exception as exc:  # noqa: BLE001
        handle_expected_error(exc, as_json=json)
        return

    # Strict mode upgrades warnings into failures.
    ok = result.valid and not (strict and result.warnings)
    payload = {
        "ok": ok,
        "file": str(path),
        "valid": result.valid,
        "errors": [issue.model_dump() for issue in result.errors],
        "warnings": [issue.model_dump() for issue in result.warnings],
    }

    if json:
        print_json(payload)
        raise typer.Exit(0 if ok else 1)

    if ok:
        print_success(f"Valid JobSpec: {path}")
        if result.warnings:
            for warning in result.warnings:
                print_warning(f"Warning [{warning.path}] {warning.message}")
        return

    print_error(f"Invalid JobSpec: {path}")
    for error in result.errors:
        print_error(f"Error [{error.path}] {error.message}")
    for warning in result.warnings:
        print_warning(f"Warning [{warning.path}] {warning.message}")
    raise typer.Exit(1)


@app.command("render")
def spec_render(
    path: Annotated[Path, typer.Argument(help="Path to a JobSpec YAML file.")],
    format: Annotated[str, typer.Option("--format", help="Render format.")] = "markdown",
    output: Annotated[
        Path | None, typer.Option("--output", help="Write output to this path.")
    ] = None,
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
    no_validate: Annotated[
        bool,
        typer.Option("--no-validate", help="Skip validation before rendering."),
    ] = False,
) -> None:
    """Render a JobSpec."""
    try:
        # Load strongly typed model first.
        spec = load_jobspec(path)
        validation = validate_spec_model(spec)
        if not no_validate and not validation.valid:
            payload = {
                "ok": False,
                "file": str(path),
                "valid": False,
                "errors": [issue.model_dump() for issue in validation.errors],
                "warnings": [issue.model_dump() for issue in validation.warnings],
            }
            if json:
                print_json(payload)
            else:
                print_error(f"Invalid JobSpec: {path}")
            raise typer.Exit(1)

        # Delegate format-specific rendering to core renderer.
        rendered = render_jobspec(spec, format=format)

        if output:
            # File output mode writes rendered content to disk.
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(rendered, encoding="utf-8")
            if json:
                print_json({"ok": True, "file": str(path), "format": format, "output": str(output)})
            else:
                print_success(f"Rendered JobSpec to {output}")
            return

        # Stdout mode prints either JSON metadata/content or raw markdown.
        if json:
            print_json({"ok": True, "file": str(path), "format": format, "content": rendered})
            return
        stdout.print(rendered, end="")
    except ValidationError as exc:
        issues = pydantic_errors_to_issues(exc)
        payload = {
            "ok": False,
            "file": str(path),
            "valid": False,
            "errors": [issue.model_dump() for issue in issues],
            "warnings": [],
        }
        if json:
            print_json(payload)
        else:
            print_error(f"Invalid JobSpec: {path}")
            for issue in issues:
                print_error(f"Error [{issue.path}] {issue.message}")
        raise typer.Exit(1)
    except Exception as exc:  # noqa: BLE001
        handle_expected_error(exc, as_json=json)


@app.command("inspect")
def spec_inspect(
    path: Annotated[Path, typer.Argument(help="Path to a JobSpec YAML file.")],
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Inspect JobSpec metadata."""
    try:
        # Reuse core inspection metadata for both human and JSON output.
        spec = load_jobspec(path)
        validation = validate_spec_model(spec)
        metadata = inspect_jobspec(spec, validation)
    except Exception as exc:  # noqa: BLE001
        handle_expected_error(exc, as_json=json)
        return

    if json:
        print_json({"ok": True, "file": str(path), "metadata": metadata})
        return

    print_kv_table(
        "JobSpec Inspection",
        [
            ("Title", str(metadata["title"])),
            ("ID", str(metadata["id"])),
            ("Schema Version", str(metadata["schema_version"])),
            ("Department", str(metadata["department"])),
            ("Level", str(metadata["level"])),
            ("Location", str(metadata["location"])),
            ("Responsibilities", str(metadata["responsibilities_count"])),
            ("Requirements", str(metadata["requirements_count"])),
            ("Nice to Have", str(metadata["nice_to_have_count"])),
            ("Valid", "yes" if bool(metadata["valid"]) else "no"),
        ],
    )


@app.command("schema")
def spec_schema(
    output: Annotated[
        Path | None, typer.Option("--output", help="Write JSON Schema to this path.")
    ] = None,
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Export the JobSpec JSON Schema."""
    try:
        schema = jobspec_json_schema()
        if output is not None:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(to_json(schema), encoding="utf-8")
            if json:
                print_json({"ok": True, "output": str(output), "schema_version": 1})
            else:
                print_success(f"Wrote schema to {output}")
            return

        if json:
            print_json({"ok": True, "schema": schema, "schema_version": 1})
            return
        stdout.print(to_json(schema))
    except Exception as exc:  # noqa: BLE001
        handle_expected_error(exc, as_json=json)
