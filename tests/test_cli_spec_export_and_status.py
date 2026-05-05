from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from neksus_jobspec_cli.main import app
from tests.spec_builders import write_export_spec

runner = CliRunner()


def test_spec_status_json_output() -> None:
    with runner.isolated_filesystem():
        target = Path("role.jobspec.yaml")
        write_export_spec(target)
        result = runner.invoke(app, ["spec", "status", str(target), "--json"])
        assert result.exit_code == 0
        payload = json.loads(result.stdout)
        assert payload["id"] == "export-role"
        assert payload["campaign_status"] == "active"
        assert payload["expires_at"] == "2026-07-03"


def test_spec_export_generic_json() -> None:
    with runner.isolated_filesystem():
        target = Path("role.jobspec.yaml")
        write_export_spec(target)
        out = Path("dist/role.json")
        result = runner.invoke(
            app,
            [
                "spec",
                "export",
                str(target),
                "--target",
                "generic-json",
                "--out",
                str(out),
                "--json",
            ],
        )
        assert result.exit_code == 0
        payload = json.loads(out.read_text(encoding="utf-8"))
        assert payload["id"] == "export-role"


def test_spec_export_generic_xml() -> None:
    with runner.isolated_filesystem():
        target = Path("role.jobspec.yaml")
        write_export_spec(target)
        out = Path("dist/role.xml")
        result = runner.invoke(
            app,
            ["spec", "export", str(target), "--target", "generic-xml", "--out", str(out)],
        )
        assert result.exit_code == 0
        content = out.read_text(encoding="utf-8")
        assert "<jobspec>" in content
        assert "<id>export-role</id>" in content


def test_spec_export_linkedin_ready_json() -> None:
    with runner.isolated_filesystem():
        target = Path("role.jobspec.yaml")
        write_export_spec(target)
        out = Path("dist/role-linkedin.json")
        result = runner.invoke(
            app,
            [
                "spec",
                "export",
                str(target),
                "--target",
                "linkedin-ready-json",
                "--out",
                str(out),
            ],
        )
        assert result.exit_code == 0
        payload = json.loads(out.read_text(encoding="utf-8"))
        assert payload["externalJobPostingId"] == "export-role"
        assert payload["validThrough"] == "2026-07-03"
