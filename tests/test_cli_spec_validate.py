from __future__ import annotations

import json
import shutil
from pathlib import Path

from typer.testing import CliRunner

from neksus.cli.main import app

runner = CliRunner()
ROOT = Path(__file__).resolve().parents[1]


def test_spec_validate_returns_zero_for_valid_jobspec() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(app, ["spec", "validate", str(target)])
        assert result.exit_code == 0
        assert "Valid JobSpec" in result.stdout


def test_spec_validate_fails_for_missing_title() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "invalid" / "missing-title.jobspec.yaml"
        target = Path("invalid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(app, ["spec", "validate", str(target)])
        assert result.exit_code == 1
        assert "Invalid JobSpec" in result.output


def test_spec_validate_json_output_shape() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(app, ["spec", "validate", str(target), "--json"])
        assert result.exit_code == 0

        payload = json.loads(result.stdout)
        assert set(payload.keys()) == {"ok", "file", "valid", "errors", "warnings"}
        assert payload["ok"] is True
        assert payload["valid"] is True
        assert payload["errors"] == []
