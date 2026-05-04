from __future__ import annotations

import json

from typer.testing import CliRunner

from neksus_jobspec_cli.main import app

runner = CliRunner()


def test_themes_lists_builtin_themes_json() -> None:
    result = runner.invoke(app, ["themes", "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    names = [theme["name"] for theme in payload["themes"]]
    assert names == ["soft-professional"]


def test_themes_show_soft_professional_json() -> None:
    result = runner.invoke(app, ["themes", "show", "soft-professional", "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["theme"]["name"] == "soft-professional"
    assert "token_hints" in payload["theme"]


def test_themes_show_unknown_fails_controlled() -> None:
    result = runner.invoke(app, ["themes", "show", "unknown", "--json"])
    assert result.exit_code == 4
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
