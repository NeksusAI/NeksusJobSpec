"""YAML parsing and JobSpec loading.

Provides safe, explicit conversion from YAML files into validated
`JobSpec` models and Neksus-specific error types.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from neksus_jobspec.errors import FileSystemError, JobSpecParseError, JobSpecValidationError
from neksus_jobspec.jobspec.models import JobSpec


def _looks_like_legacy_schema(data: dict[str, Any]) -> bool:
    legacy_markers = {"title", "summary", "responsibilities", "requirements"}
    has_legacy = any(key in data for key in legacy_markers)
    has_components_model = "job" in data or "components" in data
    return has_legacy and not has_components_model


def load_yaml_file(path: Path) -> dict[str, Any]:
    """Read a YAML file into a dictionary."""
    # Explicitly fail with a domain-specific error for missing files.
    if not path.exists():
        raise FileSystemError(f"File not found: {path}")
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise FileSystemError(f"Failed to read file: {path}") from exc
    except yaml.YAMLError as exc:
        raise JobSpecParseError(f"Invalid YAML in file: {path}") from exc

    # JobSpec documents must be YAML mappings at the top-level.
    if not isinstance(raw, dict):
        raise JobSpecParseError(f"JobSpec YAML must contain a mapping: {path}")
    return raw


def load_jobspec(path: Path) -> JobSpec:
    """Load and validate a JobSpec YAML file."""
    # Parse YAML first, then validate into the strongly typed model.
    data = load_yaml_file(path)
    try:
        return JobSpec.model_validate(data)
    except ValidationError as exc:
        if _looks_like_legacy_schema(data):
            raise JobSpecValidationError(
                f"Invalid JobSpec data in file: {path}. "
                "Legacy schema removed in 0.2.x; use component schema or migrate."
            ) from exc
        raise JobSpecValidationError(f"Invalid JobSpec data in file: {path}") from exc
