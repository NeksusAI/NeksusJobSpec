"""Validation operations for JobSpecs."""

from __future__ import annotations

from pathlib import Path

from neksus_jobspec.jobspec.parser import load_yaml_file
from neksus_jobspec.jobspec.validator import validate_spec_data


def validate_jobspec_file(path: Path, strict: bool = False) -> dict[str, object]:
    """Validate a JobSpec YAML file and normalize result payload."""
    data = load_yaml_file(path)
    result = validate_spec_data(data)
    ok = result.valid and not (strict and result.warnings)
    return {
        "ok": ok,
        "file": str(path),
        "valid": result.valid,
        "errors": [issue.model_dump() for issue in result.errors],
        "warnings": [issue.model_dump() for issue in result.warnings],
    }
