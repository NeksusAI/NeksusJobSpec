from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from neksus_jobspec_cli.main import app

runner = CliRunner()


def test_spec_schema_returns_json_payload() -> None:
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["spec", "schema", "--json"])
        assert result.exit_code == 0
        payload = json.loads(result.stdout)
        assert payload["ok"] is True
        assert payload["format"] == "json-schema"
        assert payload["schema_version"] == 1
        assert "schema" in payload
        assert payload["schema"]["$id"].endswith("jobspec.v1.json")


def test_spec_schema_writes_output_file() -> None:
    with runner.isolated_filesystem():
        out = Path("schemas/jobspec.v1.json")
        result = runner.invoke(app, ["spec", "schema", "--output", str(out)])
        assert result.exit_code == 0
        assert out.exists()
        loaded = json.loads(out.read_text(encoding="utf-8"))
        assert loaded["$id"].endswith("jobspec.v1.json")


def test_spec_schema_output_json_metadata_shape() -> None:
    with runner.isolated_filesystem():
        out = Path("schemas/jobspec.v1.json")
        result = runner.invoke(app, ["spec", "schema", "--output", str(out), "--json"])
        assert result.exit_code == 0
        payload = json.loads(result.stdout)
        assert payload == {
            "ok": True,
            "format": "json-schema",
            "schema_version": 1,
            "output": "schemas/jobspec.v1.json",
        }


def test_spec_schema_stdout_is_valid_json_schema() -> None:
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["spec", "schema"])
        assert result.exit_code == 0
        payload = json.loads(result.stdout)
        assert payload["$id"].endswith("jobspec.v1.json")
