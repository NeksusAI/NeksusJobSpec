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
from neksus.core.errors import ConfigError, FileSystemError
from neksus.core.jobspec.models import JobSpec
from neksus.core.jobspec.parser import load_yaml_file
from neksus.core.jobspec.renderer import render_jobspec
from neksus.core.jobspec.validator import validate_spec_data
from neksus.core.project.config import ProjectConfig, RenderProfile, load_project_config
from neksus.core.project.discovery import find_project_root

EXTENSIONS_BY_FORMAT = {
    "markdown": ".md",
    "html": ".html",
    "json": ".json",
}


def _output_name_for_data(data: dict, source: Path) -> str:
    spec_id = data.get("id")
    if isinstance(spec_id, str) and spec_id.strip():
        return spec_id.strip()
    return source.stem


def _resolve_profile(name: str | None, config: ProjectConfig) -> RenderProfile | None:
    if name is None:
        return None
    profile = config.render_profiles.get(name)
    if profile is None:
        raise ConfigError(f"Unknown render profile: {name}")
    return profile


def render_command(
    all_specs: Annotated[
        bool,
        typer.Option("--all", help="No-op alias kept for command clarity."),
    ] = False,
    format: Annotated[str | None, typer.Option("--format", help="Render format.")] = None,
    theme: Annotated[str | None, typer.Option("--theme", help="Built-in render theme.")] = None,
    css: Annotated[
        Path | None, typer.Option("--css", help="Append custom CSS file (HTML only).")
    ] = None,
    no_css: Annotated[
        bool, typer.Option("--no-css", help="Disable embedded CSS (HTML only).")
    ] = False,
    profile: Annotated[str | None, typer.Option("--profile", help="Render profile name.")] = None,
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
        selected_profile = _resolve_profile(profile, config)

        render_format = (
            format
            or (selected_profile.format if selected_profile else None)
            or config.default_format
        )
        selected_theme = (
            theme or (selected_profile.theme if selected_profile else None) or config.default_theme
        )
        output_directory = (
            selected_profile.output_directory if selected_profile else None
        ) or config.output_directory
        sections = (
            selected_profile.sections.model_dump()
            if selected_profile and selected_profile.sections
            else None
        )

        if (css is not None or no_css) and render_format != "html":
            raise typer.BadParameter("--css and --no-css are only supported for --format html")

        if render_format not in EXTENSIONS_BY_FORMAT:
            raise typer.BadParameter(
                f"Unsupported render format: {render_format}",
                param_hint="--format",
            )

        custom_css: str | None = None
        if css is not None:
            try:
                custom_css = css.read_text(encoding="utf-8")
            except OSError as exc:
                raise FileSystemError(f"Failed to read CSS file: {css}") from exc

        spec_dir = root / config.spec_directory
        output_dir = root / output_directory
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
            rendered_content = render_jobspec(
                spec,
                format=render_format,
                theme=selected_theme,
                embed_css=not no_css,
                custom_css=custom_css,
                sections=sections,
            )
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
            "theme": selected_theme,
            "profile": profile,
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
