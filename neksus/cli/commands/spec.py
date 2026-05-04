"""Spec commands.

This module exposes create/validate/render/inspect operations for JobSpecs.
The command layer stays thin and delegates business logic to `neksus.core`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import click
import typer
from pydantic import ValidationError

from neksus.cli.commands.common import (
    handle_expected_error,
    print_error,
    print_json,
    print_kv_table,
    print_success,
    print_warning,
)
from neksus.core.errors import ConfigError, FileSystemError, NeksusError
from neksus.core.jobspec.inspect import inspect_jobspec
from neksus.core.jobspec.migrate import inspect_schema_version
from neksus.core.jobspec.models import JobSpec
from neksus.core.jobspec.parser import load_jobspec, load_yaml_file
from neksus.core.jobspec.renderer import render_jobspec
from neksus.core.jobspec.schema import jobspec_json_schema
from neksus.core.jobspec.templates import (
    build_jobspec_template,
    dump_jobspec_yaml,
    list_template_names,
    slugify_name,
)
from neksus.core.jobspec.validator import (
    pydantic_errors_to_issues,
    validate_spec_data,
    validate_spec_model,
)
from neksus.core.output import to_json
from neksus.core.project.config import load_project_config
from neksus.core.project.discovery import find_project_root

app = typer.Typer(help="JobSpec commands")
EXPECTED_COMMAND_ERRORS = (
    typer.BadParameter,
    click.UsageError,
    NeksusError,
    OSError,
    ValidationError,
    ValueError,
)


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


def _resolve_default_theme(explicit_theme: str | None) -> str:
    """Resolve render theme with project-aware fallback."""
    if explicit_theme:
        return explicit_theme
    try:
        root = find_project_root()
        config = load_project_config(root)
        return config.default_theme
    except ConfigError:
        return "soft-professional"


@app.command("new")
def spec_new(
    name: Annotated[str, typer.Argument(help="Name used to generate JobSpec id and file name.")],
    template: Annotated[
        str,
        typer.Option("--template", help="Built-in template name."),
    ] = "basic",
    output: Annotated[Path | None, typer.Option("--output", help="Custom output path.")] = None,
    force: Annotated[bool, typer.Option("--force", help="Overwrite existing file.")] = False,
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Create a new JobSpec file."""
    try:
        if template not in list_template_names():
            raise typer.BadParameter(f"Unknown template: {template}", param_hint="--template")
        # Resolve and guard output path before writing.
        target = _resolve_new_path(name, output)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not force:
            raise FileSystemError(f"File already exists: {target}. Use --force to overwrite.")

        # Generate valid template and validate once before writing to disk.
        template_data = build_jobspec_template(name, template=template)
        JobSpec.model_validate(template_data)
        target.write_text(dump_jobspec_yaml(template_data), encoding="utf-8")
    except EXPECTED_COMMAND_ERRORS as exc:
        handle_expected_error(exc, as_json=json)
        return

    if json:
        print_json({"ok": True, "file": str(target), "template": template})
        return
    print_success(f"Created JobSpec: {target} (template: {template})")


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
    except EXPECTED_COMMAND_ERRORS as exc:
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
    format: Annotated[str, typer.Option("--format", help="Render format.")] = "web",
    theme: Annotated[str | None, typer.Option("--theme", help="Built-in render theme.")] = None,
    template: Annotated[
        str | None,
        typer.Option("--template", help="Web template preset (soft-professional)."),
    ] = None,
    css: Annotated[
        Path | None, typer.Option("--css", help="Append custom CSS file (web only).")
    ] = None,
    no_css: Annotated[
        bool, typer.Option("--no-css", help="Disable embedded CSS (web only).")
    ] = False,
    asset_base_url: Annotated[
        str | None,
        typer.Option(
            "--asset-base-url",
            help="Prefix relative component asset URLs in web output (e.g. ../examples/assets).",
        ),
    ] = None,
    output: Annotated[
        Path | None, typer.Option("--output", help="Write output to this path.")
    ] = None,
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
    no_validate: Annotated[
        bool,
        typer.Option("--no-validate", help="Skip warning checks before rendering."),
    ] = False,
) -> None:
    """Render a JobSpec."""
    try:
        if (css is not None or no_css or asset_base_url is not None) and format != "web":
            raise typer.BadParameter(
                "--css, --no-css, and --asset-base-url are only supported for --format web"
            )
        if format not in {"web", "json-ld"}:
            raise typer.BadParameter(
                "Unsupported render format. Use: web or json-ld",
                param_hint="--format",
            )
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

        selected_theme = _resolve_default_theme(theme)
        if theme is not None:
            spec.rendering.web.template = theme
        if template is not None:
            spec.rendering.web.template = template
        custom_css: str | None = None
        if css is not None:
            try:
                custom_css = css.read_text(encoding="utf-8")
            except OSError as exc:
                raise FileSystemError(f"Failed to read CSS file: {css}") from exc

        # Delegate format-specific rendering to core renderer.
        rendered = render_jobspec(
            spec,
            format=format,
            theme=selected_theme,
            embed_css=not no_css,
            custom_css=custom_css,
            asset_base_url=asset_base_url,
        )

        if output:
            # File output mode writes rendered content to disk.
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(rendered, encoding="utf-8")
            if format == "web":
                output.with_suffix(".css").write_text(
                    spec.rendering.web.css.inline, encoding="utf-8"
                )
            if json:
                print_json(
                    {
                        "ok": True,
                        "file": str(path),
                        "format": format,
                        "theme": selected_theme,
                        "output": str(output),
                        "source_format": format,
                    }
                )
            else:
                print_success(f"Rendered JobSpec to {output}")
            return

        # Stdout mode prints either JSON metadata/content or raw rendered output.
        if json:
            print_json(
                {
                    "ok": True,
                    "file": str(path),
                    "format": format,
                    "theme": selected_theme,
                    "content": rendered,
                }
            )
            return
        typer.echo(rendered, nl=False)
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
    except EXPECTED_COMMAND_ERRORS as exc:
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
    except EXPECTED_COMMAND_ERRORS as exc:
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
            ("Layout", str(metadata["layout"])),
            ("Language", str(metadata["language"])),
            ("Theme", str(metadata["theme"])),
            ("Components", str(metadata["components_count"])),
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
                print_json(
                    {
                        "ok": True,
                        "format": "json-schema",
                        "schema_version": 1,
                        "output": str(output),
                    }
                )
            else:
                print_success(f"Wrote schema to {output}")
            return

        if json:
            print_json({"ok": True, "format": "json-schema", "schema_version": 1, "schema": schema})
            return
        typer.echo(to_json(schema))
    except EXPECTED_COMMAND_ERRORS as exc:
        handle_expected_error(exc, as_json=json)


@app.command("templates")
def spec_templates(
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """List built-in JobSpec templates."""
    templates = list(list_template_names())
    if json:
        print_json({"ok": True, "templates": templates})
        return
    print_kv_table("Built-in Templates", [(name, "available") for name in templates])


@app.command("migrate")
def spec_migrate(
    path: Annotated[Path, typer.Argument(help="Path to a JobSpec YAML file.")],
    write: Annotated[
        bool,
        typer.Option("--write", help="Enable writing migrations (not implemented)."),
    ] = False,
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Inspect schema migration status for a JobSpec."""
    try:
        result = inspect_schema_version(path)
    except EXPECTED_COMMAND_ERRORS as exc:
        handle_expected_error(exc, as_json=json)
        return

    if write:
        message = "Write mode is not implemented for schema migrations."
        if json:
            print_json({"ok": False, "file": str(path), "error": message})
        else:
            print_error(message)
        raise typer.Exit(1)

    ok = result["status"] == "already_current"
    payload = {"ok": ok, "file": str(path), **result}
    if json:
        print_json(payload)
        raise typer.Exit(0 if ok else 1)

    if ok:
        print_success(f"{path}: already current (schema_version=1)")
        return
    print_warning(f"{path}: {result['message']}")
    raise typer.Exit(1)
