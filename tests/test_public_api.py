from __future__ import annotations

import importlib
from pathlib import Path

import pytest

from neksus.core.errors import JobSpecParseError, JobSpecValidationError

ROOT = Path(__file__).resolve().parents[1]


def test_import_neksus_jobspec_module() -> None:
    module = importlib.import_module("neksus_jobspec")
    assert hasattr(module, "__version__")


def test_top_level_public_imports() -> None:
    from neksus_jobspec import JobSpec, load_jobspec, render_jobspec, validate_jobspec

    assert JobSpec is not None
    assert callable(load_jobspec)
    assert callable(validate_jobspec)
    assert callable(render_jobspec)


def test_load_jobspec_returns_model_for_valid_fixture() -> None:
    from neksus_jobspec import load_jobspec

    spec = load_jobspec(ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml")
    assert spec.id == "backend-engineer"


def test_validate_jobspec_accepts_mapping() -> None:
    from neksus_jobspec import validate_jobspec

    spec = validate_jobspec(
        {
            "schema_version": 1,
            "id": "api-test",
            "title": "API Test",
            "summary": "Test summary",
            "responsibilities": ["Build things"],
            "requirements": ["Know Python"],
        }
    )
    assert spec.id == "api-test"


def test_render_jobspec_markdown_from_path() -> None:
    from neksus_jobspec import render_jobspec

    content = render_jobspec(ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml")
    assert "# Backend Engineer" in content


def test_render_jobspec_html_with_builtin_theme() -> None:
    from neksus_jobspec import render_jobspec

    content = render_jobspec(
        ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml",
        format="html",
        theme="modern",
    )
    assert "<!doctype html>" in content.lower()


def test_render_jobspec_writes_output_file(tmp_path: Path) -> None:
    from neksus_jobspec import render_jobspec

    out = tmp_path / "dist" / "backend-engineer.html"
    render_jobspec(
        ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml",
        format="html",
        theme="modern",
        output=out,
    )
    assert out.exists()


def test_load_jobspec_invalid_yaml_raises_useful_exception(tmp_path: Path) -> None:
    from neksus_jobspec import load_jobspec

    broken = tmp_path / "broken.jobspec.yaml"
    broken.write_text("schema_version: [", encoding="utf-8")

    with pytest.raises(JobSpecParseError):
        load_jobspec(broken)


def test_validate_jobspec_invalid_schema_raises_useful_exception() -> None:
    from neksus_jobspec import validate_jobspec

    with pytest.raises(JobSpecValidationError):
        validate_jobspec(
            {
                "schema_version": 1,
                "id": "invalid",
                "title": "Invalid",
                "summary": "No requirements",
                "responsibilities": ["Build things"],
                "requirements": [],
            }
        )
