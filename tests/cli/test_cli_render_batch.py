from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from neksus_jobspec_cli.main import app

runner = CliRunner()


def test_render_batch_web_renders_all_specs() -> None:
    with runner.isolated_filesystem():
        assert runner.invoke(app, ["init"]).exit_code == 0
        assert runner.invoke(app, ["spec", "new", "backend-engineer"]).exit_code == 0

        result = runner.invoke(app, ["render", "--format", "web", "--theme", "soft-professional"])
        assert result.exit_code == 0
        assert Path("dist/example.html").exists()
        assert Path("dist/backend-engineer.html").exists()
        assert "<!doctype html>" in Path("dist/example.html").read_text(encoding="utf-8").lower()


def test_render_batch_uses_jobspec_id_for_output_file() -> None:
    with runner.isolated_filesystem():
        assert runner.invoke(app, ["init", "--empty"]).exit_code == 0
        Path("jobspecs/weird-name.jobspec.yaml").write_text(
            """schema_version: 1
id: canonical-id
page:
  layout: job_detail
job:
  title: Canonical Role
  intro: Summary
components:
  - type: hero
    id: hero
    variant: default
    title: Canonical Role
    intro: Summary
  - type: list
    id: responsibilities
    variant: bullets
    title: Responsibilities
    items:
      - One
""",
            encoding="utf-8",
        )

        result = runner.invoke(app, ["render", "--format", "web"])
        assert result.exit_code == 0
        assert Path("dist/canonical-id.html").exists()
        assert not Path("dist/weird-name.html").exists()


def test_render_batch_web_summary_and_invalid_spec_exit_one() -> None:
    with runner.isolated_filesystem():
        assert runner.invoke(app, ["init"]).exit_code == 0
        Path("jobspecs/invalid.jobspec.yaml").write_text(
            """schema_version: 1
id: invalid
page:
  layout: job_detail
job:
  title: Invalid
components:
  - type: list
    id: requirements
    variant: bullets
    title: Requirements
    items: []
""",
            encoding="utf-8",
        )

        result = runner.invoke(
            app, ["render", "--format", "web", "--theme", "soft-professional", "--json"]
        )
        assert result.exit_code == 1
        payload = json.loads(result.stdout)
        assert payload["ok"] is False
        assert payload["format"] == "web"
        assert payload["theme"] == "soft-professional"
        assert isinstance(payload["rendered"], list)
        assert isinstance(payload["errors"], list)
        assert isinstance(payload["warnings"], list)


def test_render_batch_clean_removes_old_outputs() -> None:
    with runner.isolated_filesystem():
        assert runner.invoke(app, ["init", "--empty"]).exit_code == 0
        Path("jobspecs/role.jobspec.yaml").write_text(
            """schema_version: 1
id: role
page:
  layout: job_detail
job:
  title: Role
  intro: Summary
components:
  - type: hero
    id: hero
    variant: default
    title: Role
    intro: Summary
  - type: list
    id: responsibilities
    variant: bullets
    title: Responsibilities
    items:
      - One
""",
            encoding="utf-8",
        )
        Path("dist/old-file.html").parent.mkdir(parents=True, exist_ok=True)
        Path("dist/old-file.html").write_text("old", encoding="utf-8")

        result = runner.invoke(app, ["render", "--format", "web", "--clean"])
        assert result.exit_code == 0
        assert not Path("dist/old-file.html").exists()
        assert Path("dist/role.html").exists()


def test_render_batch_web_theme_pipeline_embeds_theme_styles() -> None:
    with runner.isolated_filesystem():
        assert runner.invoke(app, ["init", "--empty"]).exit_code == 0
        Path("jobspecs/role.jobspec.yaml").write_text(
            """schema_version: 1
id: role
page:
  layout: job_detail
job:
  title: Role
  intro: Summary
components:
  - type: hero
    id: hero
    variant: default
    title: Role
    intro: Summary
  - type: list
    id: responsibilities
    variant: bullets
    title: Responsibilities
    items:
      - One
""",
            encoding="utf-8",
        )
        result = runner.invoke(app, ["render", "--format", "web", "--theme", "soft-professional"])
        assert result.exit_code == 0
        content = Path("dist/role.html").read_text(encoding="utf-8")
        assert "<style>" in content


def test_render_batch_profile_and_cli_overrides() -> None:
    with runner.isolated_filesystem():
        assert runner.invoke(app, ["init", "--empty"]).exit_code == 0
        Path("jobspecs/role.jobspec.yaml").write_text(
            """schema_version: 1
id: role
page:
  layout: job_detail
job:
  title: Role
  intro: Summary
components:
  - type: hero
    id: hero
    variant: default
    title: Role
    intro: Summary
  - type: list
    id: responsibilities
    variant: bullets
    title: Responsibilities
    items:
      - One
""",
            encoding="utf-8",
        )
        Path(".neksus/config.yaml").write_text(
            """version: 1
spec_directory: jobspecs
output_directory: dist
default_format: web
strict_validation: false
default_theme: soft-professional
render_profiles:
  public:
    format: web
    theme: soft-professional
    output_directory: dist/public
    sections:
      summary: true
      details: false
      responsibilities: true
      requirements: true
      nice_to_have: false
""",
            encoding="utf-8",
        )

        profile_result = runner.invoke(app, ["render", "--profile", "public", "--json"])
        assert profile_result.exit_code == 0
        payload = json.loads(profile_result.stdout)
        assert payload["theme"] == "soft-professional"
        assert payload["profile"] == "public"

        rendered = Path("dist/public/role.html").read_text(encoding="utf-8")
        assert "Nice to Have" not in rendered

        override_result = runner.invoke(
            app,
            ["render", "--profile", "public", "--format", "web", "--theme", "classic-dark"],
        )
        assert override_result.exit_code == 0
        html = Path("dist/public/role.html").read_text(encoding="utf-8")
        assert "<!doctype html>" in html.lower()
        assert '<html class="dark"' in html


def test_render_batch_unknown_profile_fails_with_config_error() -> None:
    with runner.isolated_filesystem():
        assert runner.invoke(app, ["init"]).exit_code == 0
        result = runner.invoke(app, ["render", "--profile", "missing", "--json"])
        assert result.exit_code == 4
        payload = json.loads(result.stdout)
        assert payload["ok"] is False
