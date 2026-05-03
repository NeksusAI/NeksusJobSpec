from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from neksus.cli.main import app

runner = CliRunner()
ROOT = Path(__file__).resolve().parents[1]


def test_cli_validate_danish_example() -> None:
    example = ROOT / "examples" / "danish-job-detail.jobspec.yaml"
    result = runner.invoke(app, ["spec", "validate", str(example)])
    assert result.exit_code == 0


def test_cli_render_danish_example_web() -> None:
    example = ROOT / "examples" / "danish-job-detail.jobspec.yaml"
    result = runner.invoke(app, ["spec", "render", str(example), "--format", "web"])
    assert result.exit_code == 0
    assert "Senior Security Engineering Manager" in result.stdout


def test_cli_render_danish_example_json_ld() -> None:
    example = ROOT / "examples" / "danish-job-detail.jobspec.yaml"
    result = runner.invoke(app, ["spec", "render", str(example), "--format", "json-ld"])
    assert result.exit_code == 0
    assert '"@type": "JobPosting"' in result.stdout


def test_cli_render_danish_example_removed_pdf_format_fails() -> None:
    example = ROOT / "examples" / "danish-job-detail.jobspec.yaml"
    result = runner.invoke(app, ["spec", "render", str(example), "--format", "pdf"])
    assert result.exit_code == 2
