"""Application service for project discovery, config, and checks."""

from __future__ import annotations

from pathlib import Path

from neksus_jobspec.app.dtos import ConfigGetResult, ConfigSetResult, ProjectCheckResultDTO
from neksus_jobspec.app.project_context import ProjectContext
from neksus_jobspec.errors import InvalidInputError
from neksus_jobspec.project.checks import run_project_checks
from neksus_jobspec.project.config import set_config_key


class ProjectUseCase:
    """Use-case orchestration for project-level workflows."""

    def check(self, *, root: Path | None = None, strict: bool = False) -> ProjectCheckResultDTO:
        """Run project-level checks and return a normalized DTO payload."""
        context = ProjectContext.discover(root)
        result = run_project_checks(context.root, strict=strict)
        payload = {
            "ok": result.ok,
            "checks": [item.model_dump() for item in result.checks],
            "errors": [item.model_dump() for item in result.errors],
            "warnings": [item.model_dump() for item in result.warnings],
        }
        return ProjectCheckResultDTO.model_validate(payload)

    def config_get(self, key: str | None = None, *, root: Path | None = None) -> ConfigGetResult:
        """Read project config or a single config key.

        Raises:
            InvalidInputError: If the key does not exist in project config.
        """
        context = ProjectContext.discover(root)
        config = context.config.model_dump()
        if key is None:
            return ConfigGetResult(ok=True, config=config)
        if key not in config:
            raise InvalidInputError(f"Unknown config key: {key}")
        return ConfigGetResult(ok=True, key=key, value=config[key])

    def config_set(self, key: str, value: str, *, root: Path | None = None) -> ConfigSetResult:
        """Update a mutable project config key and return the updated config DTO."""
        context = ProjectContext.discover(root)
        updated = set_config_key(context.root, key, value)
        return ConfigSetResult(ok=True, config=updated.model_dump())
