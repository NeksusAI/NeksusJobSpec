from __future__ import annotations

import json
import shutil
from pathlib import Path

from typer.testing import CliRunner

from neksus.cli.main import app

runner = CliRunner()
ROOT = Path(__file__).resolve().parents[1]


def test_spec_render_prints_markdown() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(app, ["spec", "render", str(target)])
        assert result.exit_code == 0
        assert "# Backend Engineer" in result.stdout
        assert "## Summary" in result.stdout


def test_spec_render_output_writes_file() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        out_path = Path("dist/out.md")
        shutil.copy(src, target)

        result = runner.invoke(app, ["spec", "render", str(target), "--output", str(out_path)])
        assert result.exit_code == 0
        assert out_path.exists()
        assert "# Backend Engineer" in out_path.read_text(encoding="utf-8")


def test_spec_render_html_stdout() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(app, ["spec", "render", str(target), "--format", "html"])
        assert result.exit_code == 0
        assert "<!doctype html>" in result.stdout.lower()
        assert "<h1>Backend Engineer</h1>" in result.stdout
        assert "<style>" in result.stdout


def test_spec_render_html_each_theme_works() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        for theme in ["default", "compact", "modern"]:
            result = runner.invoke(
                app,
                ["spec", "render", str(target), "--format", "html", "--theme", theme],
            )
            assert result.exit_code == 0
            assert "<!doctype html>" in result.stdout.lower()


def test_spec_render_markdown_theme_compact() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(
            app,
            ["spec", "render", str(target), "--format", "markdown", "--theme", "compact"],
        )
        assert result.exit_code == 0
        assert "### Summary" in result.stdout


def test_spec_render_html_output_writes_file() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        out_path = Path("dist/out.html")
        shutil.copy(src, target)

        result = runner.invoke(
            app, ["spec", "render", str(target), "--format", "html", "--output", str(out_path)]
        )
        assert result.exit_code == 0
        assert out_path.exists()
        assert "<!doctype html>" in out_path.read_text(encoding="utf-8").lower()


def test_spec_render_html_custom_css_appended() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        css = Path("brand.css")
        css.write_text("main { border-width: 3px; }", encoding="utf-8")
        shutil.copy(src, target)

        result = runner.invoke(
            app,
            [
                "spec",
                "render",
                str(target),
                "--format",
                "html",
                "--theme",
                "modern",
                "--css",
                str(css),
            ],
        )
        assert result.exit_code == 0
        assert "main { border-width: 3px; }" in result.stdout


def test_spec_render_html_no_css_has_no_style_block() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(app, ["spec", "render", str(target), "--format", "html", "--no-css"])
        assert result.exit_code == 0
        assert "<style>" not in result.stdout


def test_spec_render_css_flags_rejected_for_non_html() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        css = Path("brand.css")
        css.write_text("x", encoding="utf-8")
        shutil.copy(src, target)

        result = runner.invoke(
            app,
            ["spec", "render", str(target), "--format", "markdown", "--css", str(css), "--json"],
        )
        assert result.exit_code == 2
        payload = json.loads(result.stdout)
        assert payload["ok"] is False


def test_spec_render_css_missing_file_fails() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(
            app,
            ["spec", "render", str(target), "--format", "html", "--css", "missing.css", "--json"],
        )
        assert result.exit_code == 3
        payload = json.loads(result.stdout)
        assert payload["ok"] is False


def test_spec_render_invalid_theme_is_controlled() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(
            app,
            ["spec", "render", str(target), "--format", "html", "--theme", "unknown", "--json"],
        )
        assert result.exit_code == 1
        payload = json.loads(result.stdout)
        assert payload["ok"] is False


def test_spec_render_unsupported_format_fails() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(app, ["spec", "render", str(target), "--format", "pdf"])
        assert result.exit_code == 1
        assert "Unsupported render format" in result.output


def test_spec_render_json_stdout() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(app, ["spec", "render", str(target), "--format", "json", "--json"])
        assert result.exit_code == 0
        payload = json.loads(result.stdout)
        assert payload["theme"] == "default"
        content = json.loads(payload["content"])
        assert content["id"] == "backend-engineer"


def test_spec_render_html_escapes_content() -> None:
    with runner.isolated_filesystem():
        target = Path("unsafe.jobspec.yaml")
        target.write_text(
            """schema_version: 1
id: unsafe
page:
  layout: job_detail
job:
  title: "<script>alert(1)</script>"
  intro: "Hello <b>world</b>"
components:
  - type: list
    id: responsibilities
    variant: bullets
    title: Responsibilities
    items:
      - "Own <tag>"
""",
            encoding="utf-8",
        )

        result = runner.invoke(app, ["spec", "render", str(target), "--format", "html"])
        assert result.exit_code == 0
        assert "<script>" not in result.stdout
        assert "&lt;script&gt;alert(1)&lt;/script&gt;" in result.stdout


def test_spec_inspect_json_output() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(app, ["spec", "inspect", str(target), "--json"])
        assert result.exit_code == 0

        payload = json.loads(result.stdout)
        assert payload["ok"] is True
        assert "metadata" in payload
        assert payload["metadata"]["id"] == "backend-engineer"
