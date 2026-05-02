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

        result = runner.invoke(app, ["spec", "render", str(target), "--format", "json"])
        assert result.exit_code == 0
        payload = json.loads(result.stdout)
        assert payload["id"] == "backend-engineer"


def test_spec_render_html_escapes_content() -> None:
    with runner.isolated_filesystem():
        target = Path("unsafe.jobspec.yaml")
        target.write_text(
            """schema_version: 1
id: unsafe
title: "<script>alert(1)</script>"
summary: "Hello <b>world</b>"
responsibilities:
  - "Own <tag>"
requirements:
  - "Ship > 1 feature"
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
