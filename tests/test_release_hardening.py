from __future__ import annotations

import importlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_public_api_functions_have_docstrings() -> None:
    module = importlib.import_module("neksus_jobspec")
    assert module.load_jobspec.__doc__
    assert module.validate_jobspec.__doc__
    assert module.render_jobspec.__doc__


def test_wheel_smoke_script_exists_and_is_executable() -> None:
    script = ROOT / "scripts" / "smoke_wheel.sh"
    assert script.exists()
    assert script.stat().st_mode & 0o111


def test_version_metadata_is_consistent() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    package_init = (ROOT / "neksus" / "__init__.py").read_text(encoding="utf-8")
    pyproject_match = re.search(r'^version = "([^"]+)"$', pyproject, re.MULTILINE)
    package_match = re.search(r'^__version__ = "([^"]+)"$', package_init, re.MULTILINE)
    assert pyproject_match is not None
    assert package_match is not None
    assert pyproject_match.group(1) == package_match.group(1)


def test_release_notes_include_current_version_heading() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    release_notes = (ROOT / "docs" / "release-notes.md").read_text(encoding="utf-8")
    pyproject_match = re.search(r'^version = "([^"]+)"$', pyproject, re.MULTILINE)
    assert pyproject_match is not None
    version = pyproject_match.group(1)
    assert f"## {version}" in release_notes
