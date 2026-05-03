"""Schema-version migration inspection helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from neksus.core.errors import JobSpecParseError
from neksus.core.jobspec.parser import load_yaml_file

CURRENT_SCHEMA_VERSION = 1


def inspect_schema_version(path: Path) -> dict[str, Any]:
    """Inspect a JobSpec file schema version and migration status."""
    data = load_yaml_file(path)
    version = data.get("schema_version")
    if not isinstance(version, int):
        raise JobSpecParseError("schema_version must be an integer")

    if version == CURRENT_SCHEMA_VERSION:
        return {
            "schema_version": version,
            "current_schema_version": CURRENT_SCHEMA_VERSION,
            "status": "already_current",
            "message": "already current",
            "upgradable": False,
        }
    if version > CURRENT_SCHEMA_VERSION:
        return {
            "schema_version": version,
            "current_schema_version": CURRENT_SCHEMA_VERSION,
            "status": "unsupported_future_version",
            "message": "unsupported future schema version",
            "upgradable": False,
        }
    return {
        "schema_version": version,
        "current_schema_version": CURRENT_SCHEMA_VERSION,
        "status": "upgrade_not_implemented",
        "message": "migration for older schema versions is not implemented",
        "upgradable": False,
    }
