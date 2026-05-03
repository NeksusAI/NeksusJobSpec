from __future__ import annotations

from pathlib import Path

import pytest

from neksus.core.errors import ConfigError
from neksus.core.project.config import load_project_config


def test_load_project_config_rejects_unknown_profile_key(tmp_path: Path) -> None:
    root = tmp_path
    config_path = root / ".neksus" / "config.yaml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        """version: 1
spec_directory: jobspecs
output_directory: dist
default_format: markdown
strict_validation: false
default_theme: default
render_profiles:
  public:
    format: html
    unknown: value
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfigError):
        load_project_config(root)


def test_load_project_config_rejects_unknown_section_name(tmp_path: Path) -> None:
    root = tmp_path
    config_path = root / ".neksus" / "config.yaml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        """version: 1
spec_directory: jobspecs
output_directory: dist
default_format: markdown
strict_validation: false
default_theme: default
render_profiles:
  public:
    format: html
    sections:
      summary: true
      unknown_section: false
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfigError):
        load_project_config(root)


def test_load_project_config_rejects_unknown_profile_theme(tmp_path: Path) -> None:
    root = tmp_path
    config_path = root / ".neksus" / "config.yaml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        """version: 1
spec_directory: jobspecs
output_directory: dist
default_format: markdown
strict_validation: false
default_theme: default
render_profiles:
  public:
    format: html
    theme: unknown
""",
        encoding="utf-8",
    )

    with pytest.raises(ConfigError):
        load_project_config(root)
