from __future__ import annotations

import json
from pathlib import Path

import pytest

from neksus_jobspec.errors import ConfigError
from neksus_jobspec.jobspec.rendering.theme_engine import load_manifest, resolve_theme_package


def test_resolve_builtin_theme_package() -> None:
    pkg = resolve_theme_package("soft-professional")
    assert pkg.theme_id == "soft-professional"
    assert pkg.manifest.template == "template.html.j2"


def test_resolve_custom_theme_package_path() -> None:
    root = Path(__file__).resolve().parents[2] / "fixtures" / "themes" / "custom-basic"
    pkg = resolve_theme_package(str(root))
    assert pkg.theme_id == "custom"
    assert pkg.root == root


def test_manifest_rejects_unknown_component(tmp_path: Path) -> None:
    theme_dir = tmp_path / "theme"
    theme_dir.mkdir()
    (theme_dir / "template.html.j2").write_text("<html></html>", encoding="utf-8")
    (theme_dir / "theme.css").write_text("body{}", encoding="utf-8")
    (theme_dir / "manifest.json").write_text(
        json.dumps(
            {
                "name": "bad",
                "template": "template.html.j2",
                "styles": ["theme.css"],
                "supported_components": ["hero", "new_component"],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ConfigError):
        load_manifest(theme_dir)


def test_manifest_rejects_missing_css_file(tmp_path: Path) -> None:
    theme_dir = tmp_path / "theme"
    theme_dir.mkdir()
    (theme_dir / "template.html.j2").write_text("<html></html>", encoding="utf-8")
    (theme_dir / "manifest.json").write_text(
        json.dumps(
            {
                "name": "bad",
                "template": "template.html.j2",
                "styles": ["missing.css"],
                "supported_components": ["hero"],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ConfigError):
        load_manifest(theme_dir)
