from __future__ import annotations

import importlib
import re
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_public_api_functions_have_docstrings() -> None:
    module = importlib.import_module("neksus_jobspec")
    public_functions = [
        ("load_jobspec", module.load_jobspec),
        ("validate_jobspec", module.validate_jobspec),
        ("render_jobspec", module.render_jobspec),
    ]
    key_element_groups = (
        ("Args:", "Parameters"),
        ("Returns:",),
        ("Raises:",),
    )

    for name, func in public_functions:
        doc = (func.__doc__ or "").strip()
        assert doc, f"{name} must have a non-empty docstring"
        assert len(doc) >= 20, f"{name} docstring is too short to be useful"
        assert any(any(token in doc for token in group) for group in key_element_groups), (
            f"{name} docstring should include at least one documentation section "
            f"({', '.join('/'.join(group) for group in key_element_groups)})"
        )


def test_wheel_smoke_script_exists_and_is_executable() -> None:
    script = ROOT / ".github" / "scripts" / "smoke_wheel.sh"
    assert script.exists()
    assert (script.stat().st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)) != 0


def test_version_metadata_is_consistent() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    package_init = (ROOT / "src" / "neksus_jobspec" / "__init__.py").read_text(encoding="utf-8")
    pyproject_match = re.search(r'^version = "([^"]+)"$', pyproject, re.MULTILINE)
    package_match = re.search(r'^__version__ = "([^"]+)"$', package_init, re.MULTILINE)
    assert pyproject_match is not None
    assert package_match is not None
    assert pyproject_match.group(1) == package_match.group(1)


def test_release_notes_include_current_version_heading() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    release_notes = (ROOT / "docs" / "project" / "release-notes.md").read_text(encoding="utf-8")
    pyproject_match = re.search(r'^version = "([^"]+)"$', pyproject, re.MULTILINE)
    assert pyproject_match is not None
    version = pyproject_match.group(1)
    assert f"## {version}" in release_notes
