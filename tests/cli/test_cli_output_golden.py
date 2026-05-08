from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from neksus_jobspec_cli.main import app
from tests.spec_builders import write_export_spec

runner = CliRunner()


def test_spec_exports_and_feeds_are_stable() -> None:
    with runner.isolated_filesystem():
        write_export_spec(Path("a.jobspec.yaml"), "a-job")
        write_export_spec(Path("b.jobspec.yaml"), "b-job", "closed")

        render_web_out = Path("dist/a.html")
        render_jsonld_out = Path("dist/a.jsonld")
        assert (
            runner.invoke(
                app,
                [
                    "spec",
                    "render",
                    "a.jobspec.yaml",
                    "--format",
                    "web",
                    "--output",
                    str(render_web_out),
                ],
            ).exit_code
            == 0
        )
        assert (
            runner.invoke(
                app,
                [
                    "spec",
                    "render",
                    "a.jobspec.yaml",
                    "--format",
                    "json-ld",
                    "--output",
                    str(render_jsonld_out),
                ],
            ).exit_code
            == 0
        )

        generic_json_out = Path("dist/a.json")
        generic_xml_out = Path("dist/a.xml")
        linkedin_out = Path("dist/a-linkedin.json")

        assert (
            runner.invoke(
                app,
                [
                    "spec",
                    "export",
                    "a.jobspec.yaml",
                    "--target",
                    "generic-json",
                    "--out",
                    str(generic_json_out),
                ],
            ).exit_code
            == 0
        )
        assert (
            runner.invoke(
                app,
                [
                    "spec",
                    "export",
                    "a.jobspec.yaml",
                    "--target",
                    "generic-xml",
                    "--out",
                    str(generic_xml_out),
                ],
            ).exit_code
            == 0
        )
        assert (
            runner.invoke(
                app,
                [
                    "spec",
                    "export",
                    "a.jobspec.yaml",
                    "--target",
                    "linkedin-ready-json",
                    "--out",
                    str(linkedin_out),
                ],
            ).exit_code
            == 0
        )

        feed_json_out = Path("dist/jobs.json")
        feed_xml_out = Path("dist/jobs.xml")
        sitemap_out = Path("dist/sitemap.xml")

        assert (
            runner.invoke(
                app,
                [
                    "feed",
                    "export",
                    "*.jobspec.yaml",
                    "--target",
                    "jobs-json",
                    "--out",
                    str(feed_json_out),
                ],
            ).exit_code
            == 0
        )
        assert (
            runner.invoke(
                app,
                [
                    "feed",
                    "export",
                    "*.jobspec.yaml",
                    "--target",
                    "jobs-xml",
                    "--out",
                    str(feed_xml_out),
                ],
            ).exit_code
            == 0
        )
        assert (
            runner.invoke(
                app,
                [
                    "feed",
                    "sitemap",
                    "*.jobspec.yaml",
                    "--base-url",
                    "https://company.dk/jobs",
                    "--out",
                    str(sitemap_out),
                    "--exclude-closed",
                ],
            ).exit_code
            == 0
        )

        generic_payload = json.loads(generic_json_out.read_text(encoding="utf-8"))
        assert generic_payload["id"] == "a-job"
        assert generic_payload["campaign"]["expires_at"] == "2026-07-03"

        linkedin_payload = json.loads(linkedin_out.read_text(encoding="utf-8"))
        assert linkedin_payload["externalJobPostingId"] == "a-job"
        assert linkedin_payload["validThrough"] == "2026-07-03"

        feed_payload = json.loads(feed_json_out.read_text(encoding="utf-8"))
        assert [job["id"] for job in feed_payload["jobs"]] == ["a-job", "b-job"]

        assert "<id>a-job</id>" in generic_xml_out.read_text(encoding="utf-8")
        assert "<id>a-job</id>" in feed_xml_out.read_text(encoding="utf-8")

        sitemap = sitemap_out.read_text(encoding="utf-8")
        assert "https://company.dk/jobs/a-job" in sitemap
        assert "https://company.dk/jobs/b-job" not in sitemap

        html = render_web_out.read_text(encoding="utf-8").lower()
        assert "<!doctype html>" in html
        jsonld = json.loads(render_jsonld_out.read_text(encoding="utf-8"))
        assert jsonld["@type"] == "JobPosting"
