"""Project initialization logic.

This module contains the file-system behavior for creating a new local
Neksus project structure.
"""

from __future__ import annotations

from pathlib import Path

from neksus.core.errors import FileSystemError
from neksus.core.jobspec.templates import build_jobspec_template, dump_jobspec_yaml
from neksus.core.project.config import ProjectConfig, config_path_from_root, save_project_config


def init_project(root: Path, empty: bool = False, force: bool = False) -> list[str]:
    """Initialize project files and folders.

    Args:
        root: Directory where the project should be initialized.
        empty: When True, skip creating the example JobSpec file.
        force: When True, overwrite existing config/example files.

    Returns:
        A list of created paths, relative to the project root.

    Raises:
        FileSystemError: If required files already exist or if file operations fail.
    """
    created: list[str] = []
    # Compute canonical paths for all artifacts created during initialization.
    config_path = config_path_from_root(root)
    jobspec_dir = root / "jobspecs"
    dist_dir = root / "dist"
    example_path = jobspec_dir / "example.jobspec.yaml"

    # Protect users from accidental overwrite unless they opted-in with --force.
    if config_path.exists() and not force:
        raise FileSystemError(f"Config already exists: {config_path}. Use --force to overwrite.")

    try:
        # Ensure project directories exist; this is idempotent with exist_ok=True.
        jobspec_dir.mkdir(parents=True, exist_ok=True)
        dist_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise FileSystemError("Failed to create project directories.") from exc

    # Write the default project config.
    save_project_config(root, ProjectConfig())
    created.extend([".neksus/config.yaml", "jobspecs", "dist"])

    if not empty:
        # Respect --force semantics for the example file too.
        if example_path.exists() and not force:
            raise FileSystemError(f"File already exists: {example_path}. Use --force to overwrite.")
        # Use the shared template generator to keep bootstrap examples valid.
        template = build_jobspec_template("example")
        try:
            example_path.write_text(dump_jobspec_yaml(template), encoding="utf-8")
        except OSError as exc:
            raise FileSystemError(f"Failed to write file: {example_path}") from exc
        created.append("jobspecs/example.jobspec.yaml")

    return created
