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

        result = runner.invoke(app, ["render", "--format", "markdown", "--theme", "compact"])
        assert result.exit_code == 0
        assert Path("dist/example.md").exists()
        assert Path("dist/backend-engineer.md").exists()
        assert "### Summary" in Path("dist/example.md").read_text(encoding="utf-8")


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
            app, ["render", "--format", "markdown", "--theme", "modern", "--json"]
        )
        assert result.exit_code == 1
        payload = json.loads(result.stdout)
        assert payload["ok"] is False
        assert payload["format"] == "markdown"
        assert payload["theme"] == "modern"
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
        Path("dist/old-file.md").parent.mkdir(parents=True, exist_ok=True)
        Path("dist/old-file.md").write_text("old", encoding="utf-8")

        result = runner.invoke(app, ["render", "--format", "markdown", "--clean"])
        assert result.exit_code == 0
        assert not Path("dist/old-file.md").exists()
        assert Path("dist/role.md").exists()


def test_render_batch_html_custom_css_and_no_css() -> None:
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
        css_path = Path("brand.css")
        css_path.write_text("body { outline: 0; }", encoding="utf-8")

        with_css = runner.invoke(
            app,
            ["render", "--format", "html", "--theme", "modern", "--css", str(css_path)],
        )
        assert with_css.exit_code == 0
        content = Path("dist/role.html").read_text(encoding="utf-8")
        assert "body { outline: 0; }" in content

        no_css = runner.invoke(app, ["render", "--format", "html", "--no-css"])
        assert no_css.exit_code == 0
        content_no_css = Path("dist/role.html").read_text(encoding="utf-8")
        assert "<style>" not in content_no_css


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
nice_to_have:
  - Bonus
""",
            encoding="utf-8",
        )
        Path(".neksus/config.yaml").write_text(
            """version: 1
spec_directory: jobspecs
output_directory: dist
default_format: markdown
strict_validation: false
default_theme: default
render_profiles:
  public:
    format: html
    theme: modern
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
        assert payload["theme"] == "modern"
        assert payload["profile"] == "public"

        rendered = Path("dist/public/role.html").read_text(encoding="utf-8")
        assert "Nice to Have" not in rendered

        override_result = runner.invoke(
            app,
            ["render", "--profile", "public", "--format", "markdown", "--theme", "compact"],
        )
        assert override_result.exit_code == 0
        md = Path("dist/public/role.md").read_text(encoding="utf-8")
        assert "### Responsibilities" in md


def test_render_batch_unknown_profile_fails_with_config_error() -> None:
    with runner.isolated_filesystem():
        assert runner.invoke(app, ["init"]).exit_code == 0
        result = runner.invoke(app, ["render", "--profile", "missing", "--json"])
        assert result.exit_code == 4
        payload = json.loads(result.stdout)
        assert payload["ok"] is False
