"""Public Python API for neksus-jobspec."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from neksus_jobspec.errors import JobSpecValidationError
from neksus_jobspec.jobspec.models import JobSpec
from neksus_jobspec.jobspec.parser import load_jobspec as _load_jobspec
from neksus_jobspec.jobspec.renderer import render_jobspec as _render_jobspec

__version__ = "0.3.0"


def load_jobspec(path: str | Path) -> JobSpec:
    """Load and validate a JobSpec YAML file.

    Args:
        path: Path to a JobSpec YAML file.

    Returns:
        A validated ``JobSpec`` model.

    Raises:
        FileSystemError: If the file cannot be read.
        JobSpecParseError: If YAML parsing fails.
        JobSpecValidationError: If validation fails.
    """
    return _load_jobspec(Path(path))


def validate_jobspec(path_or_data: str | Path | Mapping[str, Any]) -> JobSpec:
    """Validate a JobSpec from a path or mapping.

    Args:
        path_or_data: Path to a YAML file or mapping payload.

    Returns:
        A validated ``JobSpec`` model.

    Raises:
        FileSystemError: If reading from path fails.
        JobSpecParseError: If YAML parsing fails.
        JobSpecValidationError: If validation fails.
    """
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
    asset_base_url: str | None = None,
) -> str:
    """Render a JobSpec to a string.

    Args:
        spec_or_path: Validated JobSpec or YAML file path.
        format: Output format (``web`` or ``json-ld``).
        theme: Built-in theme name for web output.
        asset_base_url: Prefix for relative media/asset paths.

    Returns:
        Rendered output content as text.

    Raises:
        FileSystemError: If reading from path fails.
        JobSpecParseError: If YAML parsing fails.
        JobSpecValidationError: If validation fails.
        UnsupportedFormatError: If format is not supported.
    """
    spec = load_jobspec(spec_or_path) if isinstance(spec_or_path, (str, Path)) else spec_or_path
    return _render_jobspec(
        spec,
        format=format,
        theme=theme or "soft-professional",
        asset_base_url=asset_base_url,
    )


__all__ = ["JobSpec", "__version__", "load_jobspec", "render_jobspec", "validate_jobspec"]
