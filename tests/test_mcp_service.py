from __future__ import annotations

import json
from pathlib import Path

from neksus_jobspec_mcp.service import JobspecMcpService
from tests.spec_builders import write_export_spec


def test_mcp_service_version_payload() -> None:
    payload = JobspecMcpService().version()
    assert payload["ok"] is True
    assert payload["name"] == "neksus-jobspec"


def test_mcp_service_spec_schema_and_validate(tmp_path: Path) -> None:
    service = JobspecMcpService()
    schema_out = tmp_path / "schema.json"
    schema_payload = service.spec_schema(output=str(schema_out))
    assert schema_payload["ok"] is True
    assert schema_out.exists()

    spec_path = tmp_path / "role.jobspec.yaml"
    write_export_spec(spec_path, "role-id")
    validate_payload = service.spec_validate(str(spec_path))
    assert validate_payload["ok"] is True
    assert validate_payload["valid"] is True


def test_mcp_service_spec_render_and_export(tmp_path: Path) -> None:
    service = JobspecMcpService()
    spec_path = tmp_path / "role.jobspec.yaml"
    write_export_spec(spec_path, "role-id")

    render_payload = service.spec_render(str(spec_path), format="json-ld")
    assert render_payload["ok"] is True
    rendered = json.loads(render_payload["content"])
    assert rendered["@type"] == "JobPosting"

    out = tmp_path / "role.json"
    export_payload = service.spec_export(str(spec_path), "generic-json", str(out))
    assert export_payload["ok"] is True
    assert out.exists()


def test_mcp_service_feed_export_and_sitemap(tmp_path: Path) -> None:
    service = JobspecMcpService()
    write_export_spec(tmp_path / "a.jobspec.yaml", "a-job")
    write_export_spec(tmp_path / "b.jobspec.yaml", "b-job", "closed")

    feed_out = tmp_path / "jobs.json"
    feed = service.feed_export(
        inputs=[str(tmp_path)],
        target="jobs-json",
        out=str(feed_out),
    )
    assert feed["ok"] is True
    payload = json.loads(feed_out.read_text(encoding="utf-8"))
    assert payload["jobs"][0]["id"] == "a-job"

    sitemap_out = tmp_path / "sitemap.xml"
    sitemap = service.feed_sitemap(
        inputs=[str(tmp_path)],
        base_url="https://company.dk/jobs",
        out=str(sitemap_out),
        exclude_closed=True,
    )
    assert sitemap["ok"] is True
    content = sitemap_out.read_text(encoding="utf-8")
    assert "a-job" in content
    assert "b-job" not in content


def test_mcp_service_safe_call_maps_errors() -> None:
    payload = JobspecMcpService().safe_call("spec_validate", path="missing.jobspec.yaml")
    assert payload["ok"] is False
    assert payload["code"] == 3
