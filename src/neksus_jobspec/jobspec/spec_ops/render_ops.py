"""Render/schema operations for JobSpecs."""

from __future__ import annotations

from pathlib import Path

from neksus_jobspec.jobspec.parser import load_jobspec
from neksus_jobspec.jobspec.renderer import render_jobspec
from neksus_jobspec.jobspec.schema import jobspec_json_schema
from neksus_jobspec.jobspec.validator import validate_spec_model
from neksus_jobspec.output import to_json


def write_schema(output: Path | None = None) -> dict[str, object]:
    """Return JSON Schema payload or write schema file when output is provided."""
    schema = jobspec_json_schema()
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(to_json(schema), encoding="utf-8")
        return {"ok": True, "format": "json-schema", "schema_version": 1, "output": str(output)}
    return {"ok": True, "format": "json-schema", "schema_version": 1, "schema": schema}


def render_jobspec_file(
    path: Path,
    *,
    format: str,
    theme: str,
    no_validate: bool,
    embed_css: bool,
    custom_css: str | None,
    asset_base_url: str | None,
    output: Path | None,
) -> dict[str, object]:
    """Render a single JobSpec file and return normalized render payload.

    The payload shape is shared by CLI and MCP callers for deterministic output
    handling across stdout and file-output modes.
    """
    spec = load_jobspec(path)
    validation = validate_spec_model(spec)
    if not no_validate and not validation.valid:
        return {
            "ok": False,
            "file": str(path),
            "format": format,
            "theme": theme,
            "valid": False,
            "errors": [issue.model_dump() for issue in validation.errors],
            "warnings": [issue.model_dump() for issue in validation.warnings],
        }

    content = render_jobspec(
        spec,
        format=format,
        theme=theme,
        embed_css=embed_css,
        custom_css=custom_css,
        asset_base_url=asset_base_url,
    )
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")
        return {
            "ok": True,
            "file": str(path),
            "format": format,
            "theme": theme,
            "output": str(output),
            "inline_css": spec.rendering.web.css.inline if format == "web" else None,
        }

    return {
        "ok": True,
        "file": str(path),
        "format": format,
        "theme": theme,
        "content": content,
    }
