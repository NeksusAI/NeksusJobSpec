from __future__ import annotations

import json

from typer.testing import CliRunner

from neksus_jobspec_cli.main import app

runner = CliRunner()


def test_doctor_json_output() -> None:
    result = runner.invoke(app, ["doctor", "--json"])
    assert result.exit_code in {0, 1}
    payload = json.loads(result.stdout)
    assert "ok" in payload
    assert isinstance(payload["checks"], list)
    assert any(check["name"] == "Python version" for check in payload["checks"])
