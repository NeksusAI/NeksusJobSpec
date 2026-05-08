from __future__ import annotations

import json
import shutil
from pathlib import Path

from typer.testing import CliRunner

from neksus_jobspec_cli.main import app

runner = CliRunner()
ROOT = Path(__file__).resolve().parents[2]


def test_spec_render_prints_web_html_by_default() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "minimal-valid.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(app, ["spec", "render", str(target)])
        assert result.exit_code == 0
        assert "<!doctype html>" in result.stdout.lower()
        assert "Backend Engineer" in result.stdout


def test_spec_render_output_writes_file() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "minimal-valid.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        out_path = Path("dist/out.html")
        shutil.copy(src, target)

        result = runner.invoke(app, ["spec", "render", str(target), "--output", str(out_path)])
        assert result.exit_code == 0
        assert out_path.exists()
        assert "<!doctype html>" in out_path.read_text(encoding="utf-8").lower()


def test_spec_render_web_stdout() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "minimal-valid.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(app, ["spec", "render", str(target), "--format", "web"])
        assert result.exit_code == 0
        assert "<!doctype html>" in result.stdout.lower()
        assert "Backend Engineer" in result.stdout
        assert "<style>" in result.stdout


def test_spec_render_web_single_theme_works() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "minimal-valid.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(
            app,
            ["spec", "render", str(target), "--format", "web", "--theme", "soft-professional"],
        )
        assert result.exit_code == 0
        assert "<!doctype html>" in result.stdout.lower()


def test_spec_render_web_theme_soft_professional() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "minimal-valid.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(
            app,
            ["spec", "render", str(target), "--format", "web", "--theme", "soft-professional"],
        )
        assert result.exit_code == 0
        assert "<!doctype html>" in result.stdout.lower()


def test_spec_render_web_theme_classic() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "minimal-valid.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(
            app, ["spec", "render", str(target), "--format", "web", "--theme", "classic"]
        )
        assert result.exit_code == 0
        assert '<html class="light"' in result.stdout
        assert "Overview" in result.stdout


def test_spec_render_web_theme_classic_dark() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "minimal-valid.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(
            app, ["spec", "render", str(target), "--format", "web", "--theme", "classic-dark"]
        )
        assert result.exit_code == 0
        assert '<html class="dark"' in result.stdout
        assert "background:" in result.stdout
        assert "#141313" in result.stdout


def test_spec_render_classic_omits_missing_optional_sections() -> None:
    with runner.isolated_filesystem():
        target = Path("minimal.jobspec.yaml")
        target.write_text(
            """schema_version: 1
id: minimal-classic
page:
  layout: job_detail
job:
  title: Minimal Classic
  intro: Short intro
components:
  - type: list
    id: requirements
    variant: bullets
    title: Requirements
    items:
      - One requirement
""",
            encoding="utf-8",
        )
        result = runner.invoke(
            app, ["spec", "render", str(target), "--format", "web", "--theme", "classic"]
        )
        assert result.exit_code == 0
        assert "Application Process" not in result.stdout
        assert "Contact" not in result.stdout


def test_spec_render_web_output_writes_file() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "minimal-valid.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        out_path = Path("dist/out.html")
        shutil.copy(src, target)

        result = runner.invoke(
            app, ["spec", "render", str(target), "--format", "web", "--output", str(out_path)]
        )
        assert result.exit_code == 0
        assert out_path.exists()
        assert "<!doctype html>" in out_path.read_text(encoding="utf-8").lower()


def test_spec_render_web_theme_custom_requires_template_path() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "minimal-valid.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(
            app, ["spec", "render", str(target), "--format", "web", "--theme", "custom", "--json"]
        )
        assert result.exit_code == 4
        payload = json.loads(result.stdout)
        assert payload["ok"] is False


def test_spec_render_web_theme_custom_uses_user_css_as_theme() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "minimal-valid.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        theme_dir = ROOT / "fixtures" / "themes" / "custom-basic"
        shutil.copy(src, target)

        result = runner.invoke(
            app,
            [
                "spec",
                "render",
                str(target),
                "--format",
                "web",
                "--theme",
                str(theme_dir),
            ],
        )
        assert result.exit_code == 0
        assert "jobspec-page" in result.stdout
        assert "<style" in result.stdout.lower()
        assert 'class="jobspec-page"' in result.stdout


def test_spec_render_asset_base_url_rejected_for_non_web() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "minimal-valid.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(
            app,
            [
                "spec",
                "render",
                str(target),
                "--format",
                "json-ld",
                "--asset-base-url",
                "../assets",
                "--json",
            ],
        )
        assert result.exit_code == 2
        payload = json.loads(result.stdout)
        assert payload["ok"] is False


def test_spec_render_invalid_theme_is_controlled() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "minimal-valid.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(
            app,
            ["spec", "render", str(target), "--format", "web", "--theme", "unknown", "--json"],
        )
        assert result.exit_code == 4
        payload = json.loads(result.stdout)
        assert payload["ok"] is False


def test_spec_render_removed_format_fails_with_migration_message() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "minimal-valid.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(app, ["spec", "render", str(target), "--format", "html"])
        assert result.exit_code == 2
        assert "Use: web or json-ld" in result.output


def test_spec_render_json_stdout() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "minimal-valid.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(
            app, ["spec", "render", str(target), "--format", "json-ld", "--json"]
        )
        assert result.exit_code == 0
        payload = json.loads(result.stdout)
        assert payload["theme"] == "soft-professional"
        content = json.loads(payload["content"])
        assert content["@type"] == "JobPosting"


def test_spec_render_web_escapes_content() -> None:
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

        result = runner.invoke(app, ["spec", "render", str(target), "--format", "web"])
        assert result.exit_code == 0
        assert "<script>" not in result.stdout
        assert "&lt;script&gt;alert(1)&lt;/script&gt;" in result.stdout


def test_spec_render_json_ld_maps_campaign_valid_through() -> None:
    with runner.isolated_filesystem():
        target = Path("campaign.jobspec.yaml")
        target.write_text(
            """schema_version: 1
id: campaign
page:
  layout: job_detail
job:
  title: Campaign Role
  apply:
    method: external_url
    url: https://example.com/apply
campaign:
  starts_at: 2026-05-04
  expires_at: 2026-07-03
  status: active
components:
  - type: list
    id: requirements
    items:
      - One
""",
            encoding="utf-8",
        )
        result = runner.invoke(
            app, ["spec", "render", str(target), "--format", "json-ld", "--json"]
        )
        assert result.exit_code == 0
        payload = json.loads(result.stdout)
        content = json.loads(payload["content"])
        assert content["validThrough"] == "2026-07-03"


def test_spec_render_web_closed_notice_visible() -> None:
    with runner.isolated_filesystem():
        target = Path("closed.jobspec.yaml")
        target.write_text(
            """schema_version: 1
id: closed-role
page:
  layout: job_detail
job:
  title: Closed Role
  apply:
    method: external_url
    url: https://example.com/apply
campaign:
  status: closed
components:
  - type: list
    id: requirements
    items:
      - One
""",
            encoding="utf-8",
        )
        result = runner.invoke(app, ["spec", "render", str(target), "--format", "web"])
        assert result.exit_code == 0
        assert "This position is closed." in result.stdout


def test_spec_inspect_json_output() -> None:
    with runner.isolated_filesystem():
        src = ROOT / "fixtures" / "valid" / "minimal-valid.jobspec.yaml"
        target = Path("valid.jobspec.yaml")
        shutil.copy(src, target)

        result = runner.invoke(app, ["spec", "inspect", str(target), "--json"])
        assert result.exit_code == 0

        payload = json.loads(result.stdout)
        assert payload["ok"] is True
        assert "metadata" in payload
        assert payload["metadata"]["id"] == "backend-engineer"
