"""Spec commands.

This module exposes create/validate/render/inspect operations for JobSpecs.
The command layer stays thin and delegates business logic to `neksus_jobspec`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import click
import typer
from pydantic import ValidationError

from neksus_jobspec.app import SpecUseCase
from neksus_jobspec_cli.commands.common import (
    handle_expected_error,
    print_error,
    print_json,
    print_kv_table,
    print_success,
    print_warning,
)
from neksus_jobspec.errors import FileSystemError, NeksusError
from neksus_jobspec.jobspec.validator import pydantic_errors_to_issues
from neksus_jobspec.output import to_json

app = typer.Typer(help="JobSpec commands")
spec_use_case = SpecUseCase()
EXPECTED_COMMAND_ERRORS = (
    typer.BadParameter,
    click.UsageError,
    NeksusError,
    OSError,
    ValidationError,
    ValueError,
)


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
        if template not in spec_use_case.list_templates().templates:
            raise typer.BadParameter(f"Unknown template: {template}", param_hint="--template")
        # Resolve and guard output path before writing.
        target = spec_use_case.resolve_new_path(name, output)
        spec_use_case.create_new_file(name, template, target, force=force)
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
        service_result = spec_use_case.validate_file(path, strict=strict)
    except EXPECTED_COMMAND_ERRORS as exc:
        handle_expected_error(exc, as_json=json)
        return

    payload = service_result.model_dump()
    ok = service_result.ok

    if json:
        print_json(payload)
        raise typer.Exit(0 if ok else 1)

    if ok:
        print_success(f"Valid JobSpec: {path}")
        for warning in payload["warnings"]:
            print_warning(f"Warning [{warning['path']}] {warning['message']}")
        return

    print_error(f"Invalid JobSpec: {path}")
    for error in payload["errors"]:
        print_error(f"Error [{error['path']}] {error['message']}")
    for warning in payload["warnings"]:
        print_warning(f"Warning [{warning['path']}] {warning['message']}")
    raise typer.Exit(1)


@app.command("render")
def spec_render(
    path: Annotated[Path, typer.Argument(help="Path to a JobSpec YAML file.")],
    format: Annotated[str, typer.Option("--format", help="Render format.")] = "web",
    theme: Annotated[str | None, typer.Option("--theme", help="Built-in render theme.")] = None,
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
        selected_theme = spec_use_case.resolve_default_theme(theme)
        custom_css: str | None = None
        if css is not None:
            try:
                custom_css = css.read_text(encoding="utf-8")
            except OSError as exc:
                raise FileSystemError(f"Failed to read CSS file: {css}") from exc

        # Delegate format-specific rendering to core service.
        service_result = spec_use_case.render_file(
            path,
            format=format,
            theme=selected_theme,
            no_validate=no_validate,
            embed_css=not no_css,
            custom_css=custom_css,
            asset_base_url=asset_base_url,
            output=output,
        )
        payload = service_result.model_dump(exclude_none=True)
        if not service_result.ok:
            if json:
                print_json(payload)
            else:
                print_error(f"Invalid JobSpec: {path}")
            raise typer.Exit(1)

        if output:
            if format == "web" and service_result.inline_css is not None:
                output.with_suffix(".css").write_text(service_result.inline_css, encoding="utf-8")
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
            print_json(payload)
            return
        typer.echo(service_result.content, nl=False)
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
        payload = spec_use_case.inspect_file(path).model_dump()
    except EXPECTED_COMMAND_ERRORS as exc:
        handle_expected_error(exc, as_json=json)
        return

    if json:
        print_json(payload)
        return
    metadata = payload["metadata"]

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


@app.command("status")
def spec_status(
    path: Annotated[Path, typer.Argument(help="Path to a JobSpec YAML file.")],
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Show campaign status metadata for a JobSpec."""
    try:
        payload = spec_use_case.status_file(path).model_dump()
    except EXPECTED_COMMAND_ERRORS as exc:
        handle_expected_error(exc, as_json=json)
        return

    if json:
        print_json(payload)
        return
    print_kv_table(
        "JobSpec Status",
        [
            ("ID", payload["id"]),
            ("Title", payload["title"]),
            ("Campaign status", str(payload["campaign_status"] or "-")),
            ("Starts at", str(payload["starts_at"] or "-")),
            ("Expires at", str(payload["expires_at"] or "-")),
            (
                "Days remaining",
                str(payload["days_remaining"] if payload["days_remaining"] is not None else "-"),
            ),
        ],
    )


@app.command("export")
def spec_export(
    path: Annotated[Path, typer.Argument(help="Path to a JobSpec YAML file.")],
    target: Annotated[
        str,
        typer.Option(
            "--target",
            help="Export target: generic-json, generic-xml, linkedin-ready-json.",
        ),
    ],
    out: Annotated[Path, typer.Option("--out", help="Output path.")],
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Export a single JobSpec into deterministic machine-readable formats."""
    try:
        if target not in {"generic-json", "generic-xml", "linkedin-ready-json"}:
            raise typer.BadParameter(
                "Unsupported target. Use: generic-json, generic-xml, linkedin-ready-json",
                param_hint="--target",
            )
        payload = spec_use_case.export_file(path, target, out).model_dump()
    except EXPECTED_COMMAND_ERRORS as exc:
        handle_expected_error(exc, as_json=json)
        return

    if json:
        print_json(payload)
        return
    print_success(f"Exported {path} to {out} ({target})")
    for warning in payload["warnings"]:
        print_warning(warning)


@app.command("schema")
def spec_schema(
    output: Annotated[
        Path | None, typer.Option("--output", help="Write JSON Schema to this path.")
    ] = None,
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Export the JobSpec JSON Schema."""
    try:
        payload = spec_use_case.write_schema(output).model_dump(exclude_none=True, by_alias=True)
        if output is not None:
            if json:
                print_json(payload)
            else:
                print_success(f"Wrote schema to {output}")
            return

        if json:
            print_json(payload)
            return
        typer.echo(to_json(payload["schema"]))
    except EXPECTED_COMMAND_ERRORS as exc:
        handle_expected_error(exc, as_json=json)


@app.command("templates")
def spec_templates(
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """List built-in JobSpec templates."""
    templates = spec_use_case.list_templates().templates
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
        result = spec_use_case.migrate_status(path).model_dump()
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
