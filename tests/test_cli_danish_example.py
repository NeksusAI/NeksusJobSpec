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


def test_cli_render_danish_example_markdown() -> None:
    example = ROOT / "examples" / "danish-job-detail.jobspec.yaml"
    result = runner.invoke(app, ["spec", "render", str(example), "--format", "markdown"])
    assert result.exit_code == 0
    assert "Senior IT-Security Manager" in result.stdout


def test_cli_render_danish_example_html() -> None:
    example = ROOT / "examples" / "danish-job-detail.jobspec.yaml"
    result = runner.invoke(
        app, ["spec", "render", str(example), "--format", "html", "--theme", "modern"]
    )
    assert result.exit_code == 0
    assert "<!doctype html>" in result.stdout.lower()


def test_cli_render_danish_example_json() -> None:
    example = ROOT / "examples" / "danish-job-detail.jobspec.yaml"
    result = runner.invoke(app, ["spec", "render", str(example), "--format", "json"])
    assert result.exit_code == 0
    assert '"components"' in result.stdout
