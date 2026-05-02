"""Project config handling.

This module owns the `.neksus/config.yaml` shape, validation, loading,
and updates for mutable keys.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ValidationError

from neksus.core.errors import ConfigError, FileSystemError

ALLOWED_MUTABLE_KEYS = {
    "spec_directory",
    "output_directory",
    "default_format",
    "strict_validation",
}


class ProjectConfig(BaseModel):
    version: int = 1
    spec_directory: str = "jobspecs"
    output_directory: str = "dist"
    default_format: Literal["markdown", "html", "json"] = "markdown"
    strict_validation: bool = False


def config_path_from_root(root: Path) -> Path:
    """Return the config path for a discovered project root."""
    return root / ".neksus" / "config.yaml"


def load_project_config(root: Path) -> ProjectConfig:
    """Load and validate project configuration from disk.

    Args:
        root: Project root containing `.neksus/config.yaml`.

    Returns:
        A validated `ProjectConfig` instance.

    Raises:
        ConfigError: If the config is missing or invalid.
        FileSystemError: If the config cannot be read.
    """
    path = config_path_from_root(root)
    if not path.exists():
        raise ConfigError(f"Missing project config: {path}")
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise FileSystemError(f"Failed to read config: {path}") from exc
    except yaml.YAMLError as exc:
        raise ConfigError(f"Invalid config YAML: {path}") from exc

    # An empty config file is interpreted as an empty mapping and defaults apply.
    if raw is None:
        raw = {}
    if not isinstance(raw, dict):
        raise ConfigError("Project config must be a mapping.")
    try:
        return ProjectConfig.model_validate(raw)
    except ValidationError as exc:
        raise ConfigError("Project config is invalid.") from exc


def save_project_config(root: Path, config: ProjectConfig) -> None:
    """Persist project config to `.neksus/config.yaml`.

    Args:
        root: Project root where config is written.
        config: Validated config model to persist.

    Raises:
        FileSystemError: If writing fails.
    """
    path = config_path_from_root(root)
    try:
        # Ensure `.neksus/` exists before writing config.
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(config.model_dump(), sort_keys=False), encoding="utf-8")
    except OSError as exc:
        raise FileSystemError(f"Failed to write config: {path}") from exc


def set_config_key(root: Path, key: str, value: str) -> ProjectConfig:
    """Update a mutable project config key.

    Args:
        root: Project root directory.
        key: Config key to update.
        value: New value represented as string input from CLI.

    Returns:
        The updated, validated `ProjectConfig`.

    Raises:
        ConfigError: If key is immutable/unknown or value is invalid.
    """
    if key not in ALLOWED_MUTABLE_KEYS:
        raise ConfigError(f"Unknown or immutable config key: {key}")

    config = load_project_config(root)
    payload: dict[str, Any] = config.model_dump()

    # Parse known typed fields from string CLI input.
    if key == "strict_validation":
        lowered = value.strip().lower()
        if lowered not in {"true", "false"}:
            raise ConfigError("strict_validation must be true or false")
        payload[key] = lowered == "true"
    else:
        payload[key] = value

    try:
        updated = ProjectConfig.model_validate(payload)
    except ValidationError as exc:
        raise ConfigError("Updated config is invalid.") from exc

    save_project_config(root, updated)
    return updated
