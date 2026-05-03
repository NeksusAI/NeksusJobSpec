"""Stable public Python API for neksus-jobspec."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from neksus import __version__
from neksus.core.errors import FileSystemError, JobSpecValidationError
from neksus.core.jobspec.models import JobSpec
from neksus.core.jobspec.parser import load_jobspec as _load_jobspec
from neksus.core.jobspec.renderer import render_jobspec as _render_jobspec


def load_jobspec(path: str | Path) -> JobSpec:
    """Load and validate a JobSpec YAML file."""
    return _load_jobspec(Path(path))


def validate_jobspec(path_or_data: str | Path | Mapping[str, Any]) -> JobSpec:
    """Validate a JobSpec from a path or mapping and return a model."""
    if isinstance(path_or_data, (str, Path)):
        return load_jobspec(path_or_data)

    try:
        return JobSpec.model_validate(dict(path_or_data))
    except ValidationError as exc:
        raise JobSpecValidationError("Invalid JobSpec data.") from exc


def render_jobspec(
    spec_or_path: JobSpec | str | Path,
    format: str = "web",
    theme: str | None = None,
    output: str | Path | None = None,
    css: str | None = None,
    asset_base_url: str | None = None,
) -> str:
    """Render a JobSpec to a string, optionally writing to a file."""
    spec = load_jobspec(spec_or_path) if isinstance(spec_or_path, (str, Path)) else spec_or_path
    content = _render_jobspec(
        spec,
        format=format,
        theme=theme or "default",
        custom_css=css,
        asset_base_url=asset_base_url,
    )
    if output is not None:
        output_path = Path(output)
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(content, encoding="utf-8")
        except OSError as exc:
            raise FileSystemError(f"Failed to write file: {output_path}") from exc
    return content


__all__ = ["JobSpec", "__version__", "load_jobspec", "render_jobspec", "validate_jobspec"]
