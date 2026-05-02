from __future__ import annotations

import json

from typer.testing import CliRunner

from neksus.cli.main import app

runner = CliRunner()


def test_version_json_uses_neksus_jobspec_name() -> None:
    result = runner.invoke(app, ["version", "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["name"] == "neksus-jobspec"
