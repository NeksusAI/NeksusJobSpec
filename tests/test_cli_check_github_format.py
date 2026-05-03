from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from neksus.cli.main import app

runner = CliRunner()


def test_check_format_github_emits_annotations() -> None:
    with runner.isolated_filesystem():
        assert runner.invoke(app, ["init"]).exit_code == 0
        Path("jobspecs/invalid.jobspec.yaml").write_text(
            """schema_version: 1
id: invalid
page:
  layout: job_detail
job:
  title: Invalid
components:
  - type: list
    id: requirements
    variant: bullets
    title: Requirements
    items: []
""",
            encoding="utf-8",
        )

        result = runner.invoke(app, ["check", "--format", "github"])
        assert result.exit_code == 1
        assert "::error file=" in result.stdout


def test_check_format_github_and_json_are_mutually_exclusive() -> None:
    with runner.isolated_filesystem():
        assert runner.invoke(app, ["init"]).exit_code == 0

        result = runner.invoke(app, ["check", "--format", "github", "--json"])
        assert result.exit_code == 2
        payload = json.loads(result.stdout)
        assert payload["ok"] is False
