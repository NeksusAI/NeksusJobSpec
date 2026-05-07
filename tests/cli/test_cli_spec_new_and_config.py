from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from neksus_jobspec_cli.main import app

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


def test_config_set_accepts_default_format_web() -> None:
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["config", "set", "default_format", "web", "--json"])
        assert result.exit_code == 0
        payload = json.loads(result.stdout)
        assert payload["ok"] is True
        assert payload["config"]["default_format"] == "web"


def test_config_set_accepts_default_theme_soft_professional() -> None:
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        result = runner.invoke(
            app, ["config", "set", "default_theme", "soft-professional", "--json"]
        )
        assert result.exit_code == 0
        payload = json.loads(result.stdout)
        assert payload["ok"] is True
        assert payload["config"]["default_theme"] == "soft-professional"


def test_config_set_accepts_default_theme_classic_dark() -> None:
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["config", "set", "default_theme", "classic-dark", "--json"])
        assert result.exit_code == 0
        payload = json.loads(result.stdout)
        assert payload["ok"] is True
        assert payload["config"]["default_theme"] == "classic-dark"


def test_config_set_accepts_default_theme_custom() -> None:
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["config", "set", "default_theme", "custom", "--json"])
        assert result.exit_code == 0
        payload = json.loads(result.stdout)
        assert payload["ok"] is True
        assert payload["config"]["default_theme"] == "custom"


def test_config_set_rejects_unknown_theme() -> None:
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["config", "set", "default_theme", "fancy", "--json"])
        assert result.exit_code == 4
        payload = json.loads(result.stdout)
        assert payload["ok"] is False


def test_config_get_default_theme() -> None:
    with runner.isolated_filesystem():
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["config", "get", "default_theme", "--json"])
        assert result.exit_code == 0
        payload = json.loads(result.stdout)
        assert payload["ok"] is True
        assert payload["value"] == "soft-professional"
