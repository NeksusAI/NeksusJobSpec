from __future__ import annotations

import json

from typer.testing import CliRunner

from neksus_jobspec_cli.main import app

runner = CliRunner()


def test_themes_lists_builtin_themes_json() -> None:
    result = runner.invoke(app, ["themes", "list", "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    names = [theme["name"] for theme in payload["themes"]]
    assert sorted(names) == sorted(["classic", "classic-dark", "custom", "soft-professional"])


def test_themes_show_soft_professional_json() -> None:
    result = runner.invoke(app, ["themes", "show", "soft-professional", "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["theme"]["name"] == "soft-professional"
    assert payload["theme"]["source"] == "built-in"


def test_themes_show_custom_path_json() -> None:
    result = runner.invoke(app, ["themes", "show", "fixtures/themes/custom-basic", "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["theme"]["source"] == "filesystem/custom"


def test_themes_validate_custom_fixture_json() -> None:
    result = runner.invoke(app, ["themes", "validate", "fixtures/themes/custom-basic", "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True


def test_themes_init_then_validate() -> None:
    with runner.isolated_filesystem():
        init = runner.invoke(app, ["themes", "init", "my-theme", "--json"])
        assert init.exit_code == 0
        validate = runner.invoke(app, ["themes", "validate", "my-theme", "--json"])
        assert validate.exit_code == 0


def test_themes_show_unknown_fails_controlled() -> None:
    result = runner.invoke(app, ["themes", "show", "unknown", "--json"])
    assert result.exit_code == 4
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
