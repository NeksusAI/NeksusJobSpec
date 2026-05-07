from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from neksus_jobspec_cli.main import app

runner = CliRunner()
ROOT = Path(__file__).resolve().parents[2]


def test_cli_validate_job_detail_example() -> None:
    example = ROOT / "examples" / "job-detail.jobspec.yaml"
    result = runner.invoke(app, ["spec", "validate", str(example)])
    assert result.exit_code == 0


def test_cli_render_job_detail_example_web() -> None:
    example = ROOT / "examples" / "job-detail.jobspec.yaml"
    result = runner.invoke(app, ["spec", "render", str(example), "--format", "web"])
    assert result.exit_code == 0
    assert "<!doctype html>" in result.stdout.lower()
    assert "Senior Systems Architect" in result.stdout


def test_cli_render_job_detail_example_json_ld() -> None:
    example = ROOT / "examples" / "job-detail.jobspec.yaml"
    result = runner.invoke(app, ["spec", "render", str(example), "--format", "json-ld"])
    assert result.exit_code == 0
    assert '"@type": "JobPosting"' in result.stdout


def test_cli_render_job_detail_example_removed_pdf_format_fails() -> None:
    example = ROOT / "examples" / "job-detail.jobspec.yaml"
    result = runner.invoke(app, ["spec", "render", str(example), "--format", "pdf"])
    assert result.exit_code == 2
