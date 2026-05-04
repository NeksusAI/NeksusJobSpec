"""Project-domain public API."""

from neksus_jobspec.project.checks import require_project, run_project_checks
from neksus_jobspec.project.config import (
    ALLOWED_MUTABLE_KEYS,
    ProjectConfig,
    config_path_from_root,
    load_project_config,
    save_project_config,
    set_config_key,
)
from neksus_jobspec.project.discovery import find_project_root
from neksus_jobspec.project.init_project import init_project

__all__ = [
    "ALLOWED_MUTABLE_KEYS",
    "ProjectConfig",
    "config_path_from_root",
    "find_project_root",
    "init_project",
    "load_project_config",
    "require_project",
    "run_project_checks",
    "save_project_config",
    "set_config_key",
]
