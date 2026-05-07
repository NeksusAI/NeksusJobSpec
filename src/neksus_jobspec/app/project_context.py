"""Shared project context resolution for app use cases."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from neksus_jobspec.project.config import ProjectConfig, load_project_config
from neksus_jobspec.project.discovery import find_project_root


@dataclass(frozen=True)
class ProjectContext:
    """Resolved project root and config for use-case execution."""

    root: Path
    config: ProjectConfig

    @classmethod
    def discover(cls, start: Path | None = None) -> ProjectContext:
        """Discover project root and load project config as one typed context."""
        root = find_project_root(start)
        config = load_project_config(root)
        return cls(root=root, config=config)
