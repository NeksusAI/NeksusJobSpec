"""Project-level checks.

This module validates project-wide invariants:
- config presence/validity
- required directories
- JobSpec file validity
- duplicate JobSpec IDs
"""

from __future__ import annotations

from pathlib import Path

from neksus.core.errors import ConfigError, FileSystemError
from neksus.core.jobspec.parser import load_yaml_file
from neksus.core.jobspec.validator import validate_spec_data
from neksus.core.project.config import load_project_config
from neksus.core.results import ProjectCheck, ProjectCheckResult, ValidationIssue


def run_project_checks(root: Path, strict: bool = False) -> ProjectCheckResult:
    """Run all project checks and return a structured result.

    Args:
        root: Project root.
        strict: Whether warnings should fail checks.

    Returns:
        Aggregated project check result with checks/errors/warnings.

    Raises:
        FileSystemError: If required directories cannot be created.
    """
    checks: list[ProjectCheck] = []
    errors: list[ValidationIssue] = []
    warnings: list[ValidationIssue] = []

    # Validate config first; if invalid, load_project_config will raise.
    config = load_project_config(root)
    checks.append(ProjectCheck(name="config_exists", ok=True, message="Config found."))

    spec_dir = root / config.spec_directory
    output_dir = root / config.output_directory

    if spec_dir.exists() and spec_dir.is_dir():
        checks.append(
            ProjectCheck(name="spec_directory", ok=True, message="Spec directory exists.")
        )
    else:
        checks.append(
            ProjectCheck(name="spec_directory", ok=False, message="Spec directory missing.")
        )
        errors.append(
            ValidationIssue(
                path="spec_directory", code="missing", message="Spec directory is missing."
            )
        )

    # Output directory may be lazily created if missing.
    if not output_dir.exists():
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise FileSystemError(f"Cannot create output directory: {output_dir}") from exc
    checks.append(
        ProjectCheck(name="output_directory", ok=True, message="Output directory available.")
    )

    ids_seen: dict[str, Path] = {}
    files = sorted(spec_dir.glob("*.jobspec.yaml")) if spec_dir.exists() else []

    # Validate each spec and collect normalized issues.
    for path in files:
        data = load_yaml_file(path)
        result = validate_spec_data(data)

        for issue in result.errors:
            errors.append(
                ValidationIssue(
                    path=f"{path}:{issue.path}",
                    code=issue.code,
                    message=issue.message,
                )
            )
        for issue in result.warnings:
            warnings.append(
                ValidationIssue(
                    path=f"{path}:{issue.path}",
                    code=issue.code,
                    message=issue.message,
                )
            )

        # Duplicate check only for valid specs with a string id.
        spec_id = data.get("id")
        if result.valid and isinstance(spec_id, str):
            if spec_id in ids_seen:
                errors.append(
                    ValidationIssue(
                        path="id",
                        code="duplicate_id",
                        message=f"Duplicate JobSpec ID '{spec_id}' in {path} and {ids_seen[spec_id]}",
                    )
                )
            else:
                ids_seen[spec_id] = path

    checks.append(
        ProjectCheck(
            name="jobspec_files",
            ok=not errors,
            message="All JobSpec files valid." if not errors else "Some JobSpec files are invalid.",
        )
    )

    # Strict mode can be requested in CLI or enabled in project config.
    strict_mode = strict or config.strict_validation
    ok = not errors and not (strict_mode and warnings)
    if strict_mode and warnings:
        checks.append(
            ProjectCheck(name="strict_warnings", ok=False, message="Warnings treated as failures.")
        )

    return ProjectCheckResult(ok=ok, checks=checks, errors=errors, warnings=warnings)


def require_project(root: Path | None = None) -> Path:
    """Require a valid Neksus project and return its root."""
    from neksus.core.project.discovery import find_project_root

    try:
        return find_project_root(root)
    except ConfigError as exc:
        raise ConfigError(str(exc)) from exc
