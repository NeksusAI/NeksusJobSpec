"""Project config handling.

This module owns the `.neksus/config.yaml` shape, validation, loading,
and updates for mutable keys.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from neksus.core.errors import ConfigError, FileSystemError

ALLOWED_MUTABLE_KEYS = {
    "spec_directory",
    "output_directory",
    "default_format",
    "strict_validation",
    "default_theme",
}


class RenderSections(BaseModel):
    """Project-level render section visibility controls."""

    model_config = ConfigDict(extra="forbid")

    summary: bool = True
    details: bool = True
    responsibilities: bool = True
    requirements: bool = True
    nice_to_have: bool = True


class RenderProfile(BaseModel):
    """Project-level render profile overrides."""

    model_config = ConfigDict(extra="forbid")

    format: Literal["web", "json-ld"] | None = None
    theme: Literal["soft-professional"] | None = None
    output_directory: str | None = None
    sections: RenderSections | None = None


class ProjectConfig(BaseModel):
    version: int = 1
    spec_directory: str = "jobspecs"
    output_directory: str = "dist"
    default_format: Literal["web", "json-ld"] = "web"
    strict_validation: bool = False
    default_theme: Literal["soft-professional"] = "soft-professional"
    render_profiles: dict[str, RenderProfile] = Field(default_factory=dict)


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

    if raw is None:
        raw = {}
    if not isinstance(raw, dict):
        raise ConfigError("Project config must be a mapping.")
    try:
        return ProjectConfig.model_validate(raw)
    except ValidationError as exc:
        raise ConfigError("Project config is invalid.") from exc


def save_project_config(root: Path, config: ProjectConfig) -> None:
    """Persist project config to `.neksus/config.yaml`."""
    path = config_path_from_root(root)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(config.model_dump(), sort_keys=False), encoding="utf-8")
    except OSError as exc:
        raise FileSystemError(f"Failed to write config: {path}") from exc


def set_config_key(root: Path, key: str, value: str) -> ProjectConfig:
    """Update a mutable project config key."""
    if key not in ALLOWED_MUTABLE_KEYS:
        raise ConfigError(f"Unknown or immutable config key: {key}")

    config = load_project_config(root)
    payload: dict[str, Any] = config.model_dump()

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
