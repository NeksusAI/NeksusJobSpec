"""Migration status operations for JobSpecs."""

from __future__ import annotations

from pathlib import Path

from neksus_jobspec.jobspec.migrate import inspect_schema_version


def migrate_status(path: Path) -> dict[str, object]:
    """Inspect schema-version migration status for a JobSpec file."""
    return inspect_schema_version(path)
