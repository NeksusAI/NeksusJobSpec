from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from neksus.cli.main import app

runner = CliRunner()


def test_render_batch_markdown_renders_all_specs() -> None:
    with runner.isolated_filesystem():
        assert runner.invoke(app, ["init"]).exit_code == 0
        assert runner.invoke(app, ["spec", "new", "backend-engineer"]).exit_code == 0

        result = runner.invoke(app, ["render", "--format", "markdown"])
        assert result.exit_code == 0
        assert Path("dist/example.md").exists()
        assert Path("dist/backend-engineer.md").exists()


def test_render_batch_uses_jobspec_id_for_output_file() -> None:
    with runner.isolated_filesystem():
        assert runner.invoke(app, ["init", "--empty"]).exit_code == 0
        Path("jobspecs/weird-name.jobspec.yaml").write_text(
            """schema_version: 1
id: canonical-id
title: Canonical Role
summary: Summary
responsibilities:
  - One
requirements:
  - One
""",
            encoding="utf-8",
        )

        result = runner.invoke(app, ["render", "--format", "markdown"])
        assert result.exit_code == 0
        assert Path("dist/canonical-id.md").exists()
        assert not Path("dist/weird-name.md").exists()


def test_render_batch_json_summary_and_invalid_spec_exit_one() -> None:
    with runner.isolated_filesystem():
        assert runner.invoke(app, ["init"]).exit_code == 0
        Path("jobspecs/invalid.jobspec.yaml").write_text(
            """schema_version: 1
id: invalid
title: Invalid
summary: Summary
responsibilities:
  - One
requirements: []
""",
            encoding="utf-8",
        )

        result = runner.invoke(app, ["render", "--format", "markdown", "--json"])
        assert result.exit_code == 1
        payload = json.loads(result.stdout)
        assert payload["ok"] is False
        assert payload["format"] == "markdown"
        assert isinstance(payload["rendered"], list)
        assert isinstance(payload["errors"], list)
        assert isinstance(payload["warnings"], list)


def test_render_batch_clean_removes_old_outputs() -> None:
    with runner.isolated_filesystem():
        assert runner.invoke(app, ["init", "--empty"]).exit_code == 0
        Path("jobspecs/role.jobspec.yaml").write_text(
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
        Path("dist/old-file.md").parent.mkdir(parents=True, exist_ok=True)
        Path("dist/old-file.md").write_text("old", encoding="utf-8")

        result = runner.invoke(app, ["render", "--format", "markdown", "--clean"])
        assert result.exit_code == 0
        assert not Path("dist/old-file.md").exists()
        assert Path("dist/role.md").exists()
