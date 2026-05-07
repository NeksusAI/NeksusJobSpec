from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from neksus_jobspec_cli.main import app
from ..spec_builders import write_export_spec

runner = CliRunner()


def test_feed_export_jobs_json_deterministic() -> None:
    with runner.isolated_filesystem():
        write_export_spec(Path("b.jobspec.yaml"), "b-job")
        write_export_spec(Path("a.jobspec.yaml"), "a-job")
        out = Path("dist/jobs.json")
        result = runner.invoke(
            app,
            [
                "feed",
                "export",
                "*.jobspec.yaml",
                "--target",
                "jobs-json",
                "--out",
                str(out),
            ],
        )
        assert result.exit_code == 0
        payload = json.loads(out.read_text(encoding="utf-8"))
        assert payload["jobs"][0]["id"] == "a-job"
        assert payload["jobs"][1]["id"] == "b-job"


def test_feed_export_jobs_xml() -> None:
    with runner.isolated_filesystem():
        write_export_spec(Path("a.jobspec.yaml"), "a-job")
        write_export_spec(Path("b.jobspec.yaml"), "b-job")
        out = Path("dist/jobs.xml")
        result = runner.invoke(
            app,
            ["feed", "export", "*.jobspec.yaml", "--target", "jobs-xml", "--out", str(out)],
        )
        assert result.exit_code == 0
        content = out.read_text(encoding="utf-8")
        assert "<jobs" in content
        assert "<id>a-job</id>" in content


def test_feed_export_invalid_fails_by_default() -> None:
    with runner.isolated_filesystem():
        write_export_spec(Path("ok.jobspec.yaml"), "ok-job")
        Path("bad.jobspec.yaml").write_text("id: bad", encoding="utf-8")
        result = runner.invoke(
            app,
            [
                "feed",
                "export",
                "*.jobspec.yaml",
                "--target",
                "jobs-json",
                "--out",
                "dist/jobs.json",
            ],
        )
        assert result.exit_code == 1


def test_feed_sitemap_generation_and_filter() -> None:
    with runner.isolated_filesystem():
        write_export_spec(Path("open.jobspec.yaml"), "open-job", "active")
        write_export_spec(Path("closed.jobspec.yaml"), "closed-job", "closed")
        out = Path("dist/sitemap.xml")
        result = runner.invoke(
            app,
            [
                "feed",
                "sitemap",
                "*.jobspec.yaml",
                "--base-url",
                "https://company.dk/jobs",
                "--out",
                str(out),
                "--exclude-closed",
            ],
        )
        assert result.exit_code == 0
        content = out.read_text(encoding="utf-8")
        assert "https://company.dk/jobs/open-job" in content
        assert "https://company.dk/jobs/closed-job" not in content
