from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from neksus.cli.main import app

runner = CliRunner()


def test_spec_new_backend_engineer_creates_valid_file() -> None:
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["spec", "new", "backend-engineer"])
        assert result.exit_code == 0
        target = Path("jobspecs/backend-engineer.jobspec.yaml")
        assert target.exists()

        validate_result = runner.invoke(app, ["spec", "validate", str(target)])
        assert validate_result.exit_code == 0


def test_config_set_rejects_unknown_key() -> None:
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["config", "set", "unknown_key", "value", "--json"])
        payload = json.loads(result.stdout)
        assert result.exit_code != 0
        assert payload["ok"] is False


def test_config_set_accepts_default_format_html() -> None:
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["config", "set", "default_format", "html", "--json"])
        assert result.exit_code == 0
        payload = json.loads(result.stdout)
        assert payload["ok"] is True
        assert payload["config"]["default_format"] == "html"
