from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
CLI_BIN = ROOT / ".venv" / "bin" / "neksus-jobspec"


@pytest.mark.integration
def test_integration_init_and_validate_flow(tmp_path: Path) -> None:
    subprocess.run([str(CLI_BIN), "init", "--empty"], cwd=tmp_path, check=True)
    jobspecs = tmp_path / "jobspecs"
    jobspecs.mkdir(exist_ok=True)
    shutil.copy(
        ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml",
        jobspecs / "backend-engineer.jobspec.yaml",
    )

    validate = subprocess.run(
        [str(CLI_BIN), "spec", "validate", str(jobspecs / "backend-engineer.jobspec.yaml")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert validate.returncode == 0
    assert "Valid JobSpec" in validate.stdout


@pytest.mark.integration
def test_integration_render_web_with_css_flow(tmp_path: Path) -> None:
    subprocess.run([str(CLI_BIN), "init", "--empty"], cwd=tmp_path, check=True)
    jobspec = tmp_path / "jobspecs" / "backend-engineer.jobspec.yaml"
    jobspec.parent.mkdir(exist_ok=True)
    shutil.copy(ROOT / "fixtures" / "valid" / "backend-engineer.jobspec.yaml", jobspec)

    out_file = tmp_path / "dist" / "backend-engineer.html"
    subprocess.run(
        [
            str(CLI_BIN),
            "spec",
            "render",
            str(jobspec),
            "--format",
            "web",
            "--theme",
            "soft-professional",
            "--css",
            str(ROOT / "examples" / "jobspec.css"),
            "--output",
            str(out_file),
        ],
        cwd=tmp_path,
        check=True,
    )

    assert out_file.exists()
    html = out_file.read_text(encoding="utf-8")
    assert "<html" in html
    assert "font-family" in html


@pytest.mark.integration
def test_integration_check_and_strict_behavior_flow(tmp_path: Path) -> None:
    subprocess.run([str(CLI_BIN), "init", "--empty"], cwd=tmp_path, check=True)
    jobspec = tmp_path / "jobspecs" / "warning.jobspec.yaml"
    jobspec.parent.mkdir(exist_ok=True)
    jobspec.write_text(
        """schema_version: 1
id: warning-role
page:
  layout: job_detail
job:
  title: Dev
  intro: Summary
components:
  - type: list
    id: responsibilities
    variant: bullets
    title: Responsibilities
    items:
      - Build APIs.
      - build apis.
""",
        encoding="utf-8",
    )

    check_default = subprocess.run(
        [str(CLI_BIN), "check", "--json"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert check_default.returncode == 0
    default_payload = json.loads(check_default.stdout)
    assert default_payload["ok"] is True

    check_strict = subprocess.run(
        [str(CLI_BIN), "check", "--strict", "--json"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert check_strict.returncode == 1
    payload = json.loads(check_strict.stdout)
    assert payload["ok"] is False
    assert payload["warnings"]


@pytest.mark.integration
def test_integration_schema_export_flow(tmp_path: Path) -> None:
    subprocess.run([str(CLI_BIN), "init", "--empty"], cwd=tmp_path, check=True)
    schema_path = tmp_path / "schemas" / "jobspec.v1.json"

    subprocess.run(
        [str(CLI_BIN), "spec", "schema", "--output", str(schema_path)],
        cwd=tmp_path,
        check=True,
    )

    assert schema_path.exists()
    payload = json.loads(schema_path.read_text(encoding="utf-8"))
    assert payload.get("title") == "Neksus JobSpec"
    assert payload.get("type") == "object"


@pytest.mark.integration
def test_integration_batch_render_profile_flow(tmp_path: Path) -> None:
    subprocess.run([str(CLI_BIN), "init", "--empty"], cwd=tmp_path, check=True)
    jobspec = tmp_path / "jobspecs" / "role.jobspec.yaml"
    jobspec.parent.mkdir(exist_ok=True)
    jobspec.write_text(
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

    config_path = tmp_path / ".neksus" / "config.yaml"
    config_path.write_text(
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

    render = subprocess.run(
        [str(CLI_BIN), "render", "--profile", "public", "--json"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert render.returncode == 0
    payload = json.loads(render.stdout)
    assert payload["ok"] is True
    assert payload["profile"] == "public"
    assert payload["theme"] == "soft-professional"

    html_file = tmp_path / "dist" / "public" / "role.html"
    assert html_file.exists()
    html = html_file.read_text(encoding="utf-8")
    assert "Nice to Have" not in html
