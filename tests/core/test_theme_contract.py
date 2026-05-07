from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from neksus_jobspec.errors import ConfigError
from neksus_jobspec.jobspec.models import JobSpec
from neksus_jobspec.jobspec.rendering.html import render_html
from neksus_jobspec.jobspec.rendering.options import RenderOptions
from neksus_jobspec.jobspec.rendering.theme_contract import (
    GLOBAL_MANDATORY_COMPONENT_TYPES,
    build_theme_render_context,
)
from neksus_jobspec.jobspec.rendering.theme_engine import (
    resolve_theme_package,
    validate_theme_package,
)

ROOT = Path(__file__).resolve().parents[2]


def _load_fixture(name: str = "minimal-valid.jobspec.yaml") -> JobSpec:
    path = ROOT / "fixtures" / "valid" / name
    return JobSpec.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")))


def test_theme_render_context_shape() -> None:
    spec = _load_fixture()
    options = RenderOptions(format="web", theme="soft-professional")
    context = build_theme_render_context(spec, options)

    assert context.theme == "soft-professional"
    assert context.components
    assert context.components_by_region
    assert set(context.mandatory.required) == set(GLOBAL_MANDATORY_COMPONENT_TYPES)
    assert set(context.mandatory.present).issubset(set(context.mandatory.required))


def test_builtin_theme_package_validates_against_contract() -> None:
    spec = _load_fixture()
    options = RenderOptions(format="web", theme="soft-professional")
    context = build_theme_render_context(spec, options)
    package = resolve_theme_package("soft-professional")
    validate_theme_package(package, context)


def test_custom_theme_package_validates_against_contract() -> None:
    spec = _load_fixture()
    theme_root = ROOT / "fixtures" / "themes" / "custom-basic"
    options = RenderOptions(format="web", theme=str(theme_root))
    context = build_theme_render_context(spec, options)
    package = resolve_theme_package(str(theme_root))
    validate_theme_package(package, context)


def test_missing_mandatory_wiring_fails_validation(tmp_path: Path) -> None:
    theme_dir = tmp_path / "theme"
    theme_dir.mkdir()
    (theme_dir / "template.html.j2").write_text("<html>{{ title }}</html>", encoding="utf-8")
    (theme_dir / "theme.css").write_text("body{}", encoding="utf-8")
    (theme_dir / "manifest.json").write_text(
        """{
  "name": "bad-theme",
  "version": 1,
  "template": "template.html.j2",
  "styles": ["theme.css"],
  "supported_components": ["hero", "list"],
  "supported_regions": ["header", "hero", "main", "sidebar", "footer"]
}""",
        encoding="utf-8",
    )
    spec = _load_fixture()
    options = RenderOptions(format="web", theme=str(theme_dir))
    context = build_theme_render_context(spec, options)
    package = resolve_theme_package(str(theme_dir))

    with pytest.raises(ConfigError, match="must support mandatory components"):
        validate_theme_package(package, context)


def test_unified_render_path_supports_builtin_and_custom() -> None:
    spec = _load_fixture()
    built_in_html = render_html(spec, RenderOptions(format="web", theme="classic"))
    assert "Overview" in built_in_html

    theme_root = ROOT / "fixtures" / "themes" / "custom-basic"
    custom_html = render_html(spec, RenderOptions(format="web", theme=str(theme_root)))
    assert "jobspec-page" in custom_html
