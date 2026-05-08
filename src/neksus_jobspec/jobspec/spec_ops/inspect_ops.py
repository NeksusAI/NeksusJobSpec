"""Inspect/status operations for JobSpecs."""

from __future__ import annotations

from pathlib import Path

from neksus_jobspec.jobspec.inspect import inspect_jobspec
from neksus_jobspec.jobspec.lint import lint_jobspec
from neksus_jobspec.jobspec.parser import load_jobspec
from neksus_jobspec.jobspec.validator import validate_spec_model


def inspect_jobspec_file(path: Path) -> dict[str, object]:
    """Inspect metadata for a validated JobSpec file."""
    spec = load_jobspec(path)
    validation = validate_spec_model(spec)
    metadata = inspect_jobspec(spec, validation)
    return {"ok": True, "file": str(path), "metadata": metadata}


def status_jobspec_file(path: Path) -> dict[str, object]:
    """Return campaign/status metadata payload for a JobSpec file."""
    spec = load_jobspec(path)
    warnings = lint_jobspec(spec)
    return {
        "ok": True,
        "file": str(path),
        **spec.campaign_status_payload(),
        "warnings": [warning.model_dump() for warning in warnings],
    }
