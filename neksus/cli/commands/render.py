"""Batch project render command."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Annotated

import typer

from neksus.cli.commands.common import (
    handle_expected_error,
    print_error,
    print_json,
    print_success,
)
from neksus.core.errors import FileSystemError
from neksus.core.jobspec.models import JobSpec
from neksus.core.jobspec.parser import load_yaml_file
from neksus.core.jobspec.renderer import render_jobspec
from neksus.core.jobspec.validator import validate_spec_data
from neksus.core.project.config import load_project_config
from neksus.core.project.discovery import find_project_root

EXTENSIONS_BY_FORMAT = {
    "markdown": ".md",
    "html": ".html",
    "json": ".json",
}


def _render_format_from_option(option: str | None, default_format: str) -> str:
    if option:
        return option
    return default_format


def _output_name_for_data(data: dict, source: Path) -> str:
    spec_id = data.get("id")
    if isinstance(spec_id, str) and spec_id.strip():
        return spec_id.strip()
    return source.stem


def render_command(
    all_specs: Annotated[
        bool,
        typer.Option("--all", help="No-op alias kept for command clarity."),
    ] = False,
    format: Annotated[str | None, typer.Option("--format", help="Render format.")] = None,
    clean: Annotated[
        bool,
        typer.Option("--clean", help="Remove output directory before render."),
    ] = False,
    json: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON.")] = False,
) -> None:
    """Render all project JobSpecs into configured output directory."""
    _ = all_specs
    try:
        root = find_project_root()
        config = load_project_config(root)
        render_format = _render_format_from_option(format, config.default_format)
        if render_format not in EXTENSIONS_BY_FORMAT:
            raise typer.BadParameter(
                f"Unsupported render format: {render_format}",
                param_hint="--format",
            )

        spec_dir = root / config.spec_directory
        output_dir = root / config.output_directory
        if not spec_dir.exists() or not spec_dir.is_dir():
            raise FileSystemError(f"Spec directory does not exist: {spec_dir}")

        if clean and output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        files = sorted(spec_dir.glob("*.jobspec.yaml"))
        rendered: list[dict[str, str]] = []
        errors: list[dict[str, str]] = []
        warnings: list[dict[str, str]] = []

        for path in files:
            data = load_yaml_file(path)
            validation = validate_spec_data(data)

            for issue in validation.errors:
                errors.append({"source": str(path.relative_to(root)), **issue.model_dump()})
            for issue in validation.warnings:
                warnings.append({"source": str(path.relative_to(root)), **issue.model_dump()})
            if not validation.valid:
                continue

            target_name = _output_name_for_data(data, path)
            target = output_dir / f"{target_name}{EXTENSIONS_BY_FORMAT[render_format]}"
            spec = JobSpec.model_validate(data)
            rendered_content = render_jobspec(spec, format=render_format)
            target.write_text(rendered_content, encoding="utf-8")
            rendered.append(
                {
                    "source": str(path.relative_to(root)),
                    "output": str(target.relative_to(root)),
                }
            )

        ok = not errors
        payload = {
            "ok": ok,
            "format": render_format,
            "rendered": rendered,
            "errors": errors,
            "warnings": warnings,
        }
        if json:
            print_json(payload)
            raise typer.Exit(0 if ok else 1)

        if ok:
            print_success(f"Rendered {len(rendered)} JobSpec files to {output_dir}")
            return
        print_error("Batch render failed: one or more JobSpec files are invalid.")
        raise typer.Exit(1)
    except typer.Exit:
        raise
    except Exception as exc:  # noqa: BLE001
        handle_expected_error(exc, as_json=json)
