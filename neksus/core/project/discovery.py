"""Project root discovery.

Provides upward-directory traversal to locate a Neksus project root by
detecting `.neksus/config.yaml`.
"""

from __future__ import annotations

from pathlib import Path

from neksus.core.errors import ConfigError


def find_project_root(start: Path | None = None) -> Path:
    """Find project root by walking upward for `.neksus/config.yaml`.

    Args:
        start: Optional starting directory. Defaults to current working directory.

    Returns:
        The discovered project root path.

    Raises:
        ConfigError: If no project root is found.
    """
    current = (start or Path.cwd()).resolve()

    # Search current directory first, then each parent directory.
    for candidate in [current, *current.parents]:
        if (candidate / ".neksus" / "config.yaml").exists():
            return candidate

    raise ConfigError("No Neksus project found. Run `neksus-jobspec init` first.")
