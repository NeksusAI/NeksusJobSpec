from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from neksus.cli.main import app

runner = CliRunner()


def test_spec_migrate_reports_already_current() -> None:
    with runner.isolated_filesystem():
        path = Path("current.jobspec.yaml")
        path.write_text(
            """schema_version: 1
id: role
title: Role
summary: Summary
responsibilities:
  - One
requirements:
  - One
""",
            encoding="utf-8",
        )

        result = runner.invoke(app, ["spec", "migrate", str(path), "--json"])
        assert result.exit_code == 0
        payload = json.loads(result.stdout)
        assert payload["status"] == "already_current"


def test_spec_migrate_refuses_future_schema_version() -> None:
    with runner.isolated_filesystem():
        path = Path("future.jobspec.yaml")
        path.write_text(
            """schema_version: 2
id: role
title: Role
summary: Summary
responsibilities:
  - One
requirements:
  - One
""",
            encoding="utf-8",
        )

        result = runner.invoke(app, ["spec", "migrate", str(path), "--json"])
        assert result.exit_code == 1
        payload = json.loads(result.stdout)
        assert payload["status"] == "unsupported_future_version"


def test_spec_migrate_write_not_implemented() -> None:
    with runner.isolated_filesystem():
        path = Path("current.jobspec.yaml")
        path.write_text(
            """schema_version: 1
id: role
title: Role
summary: Summary
responsibilities:
  - One
requirements:
  - One
""",
            encoding="utf-8",
        )

        result = runner.invoke(app, ["spec", "migrate", str(path), "--write", "--json"])
        assert result.exit_code == 1
        payload = json.loads(result.stdout)
        assert payload["ok"] is False
