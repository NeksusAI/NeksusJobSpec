"""Lint operations for JobSpecs."""

from __future__ import annotations

from pathlib import Path

from neksus_jobspec.jobspec.lint import lint_jobspec
from neksus_jobspec.jobspec.parser import load_jobspec


def lint_jobspec_file(path: Path) -> dict[str, object]:
    """Run advisory lint checks on one valid JobSpec file."""
    spec = load_jobspec(path)
    warnings = lint_jobspec(spec)
    return {
        "ok": True,
        "file": str(path),
        "warnings": [warning.model_dump() for warning in warnings],
    }
