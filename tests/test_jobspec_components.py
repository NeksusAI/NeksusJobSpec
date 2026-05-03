from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from neksus.core.jobspec.models import JobSpec
from neksus.core.jobspec.renderer import render_jobspec

ROOT = Path(__file__).resolve().parents[1]


def _component_spec() -> dict:
    return {
        "schema_version": 1,
        "id": "danish-security-manager",
        "page": {
            "layout": "job_detail",
            "language": "da",
            "theme": "modern",
            "component_order": ["hero", "facts", "process", "contact"],
        },
        "job": {
            "title": "Senior IT-Security Manager",
            "intro": "Vil du være med til at styrke vores sikkerhed?",
            "apply": {"label": "Send ansøgning", "url": "https://example.com/apply"},
        },
        "components": [
            {
                "type": "hero",
                "id": "hero",
                "variant": "split",
                "title": "Senior IT-Security Manager",
                "intro": "Vil du være med til at styrke vores sikkerhed?",
            },
            {
                "type": "facts",
                "id": "facts",
                "variant": "sidebar",
                "title": "Jobdetaljer",
                "items": [
                    {"label": "Region", "value": "Region Hovedstaden"},
                    {"label": "Jobtype", "value": "Fast"},
                ],
            },
            {
                "type": "application_process",
                "id": "process",
                "variant": "steps",
                "title": "Sådan søger du",
                "deadline": "04-05-2026",
                "steps": ["Upload CV", "Samtale", "Tilbud"],
            },
            {
                "type": "contact",
                "id": "contact",
                "variant": "card",
                "title": "Har du spørgsmål?",
                "name": "Anna Hansen",
                "email": "anna@example.com",
                "class_name": "contact-card",
                "attributes": {"data-region": "dk"},
            },
        ],
        "rendering": {
            "html": {
                "facts_position": "sidebar",
                "repeat_cta": True,
                "show_share_links": True,
                "show_print_link": True,
            },
            "css": {"files": [], "inline": ".job { color: black; }", "tokens": {}},
            "js": {
                "files": ["/static/app.js"],
                "inline": "console.log('x')",
                "allow_inline": False,
            },
        },
    }


def test_legacy_jobspec_no_longer_validates() -> None:
    with pytest.raises(ValidationError):
        JobSpec.model_validate(
            {
                "schema_version": 1,
                "id": "backend-engineer",
                "title": "Backend Engineer",
                "summary": "Build systems.",
                "responsibilities": ["Build APIs"],
                "requirements": ["Python"],
            }
        )


def test_component_jobspec_validates() -> None:
    spec = JobSpec.model_validate(_component_spec())
    assert spec.job is not None
    assert len(spec.components) == 4


def test_invalid_component_type_fails() -> None:
    data = _component_spec()
    data["components"][0]["type"] = "unknown"
    with pytest.raises(ValidationError):
        JobSpec.model_validate(data)


def test_invalid_variant_fails() -> None:
    data = _component_spec()
    data["components"][0]["variant"] = "bad"
    with pytest.raises(ValidationError):
        JobSpec.model_validate(data)


def test_duplicate_component_ids_fail() -> None:
    data = _component_spec()
    data["components"][1]["id"] = "hero"
    with pytest.raises(ValidationError):
        JobSpec.model_validate(data)


def test_component_order_missing_id_fails() -> None:
    data = _component_spec()
    data["page"]["component_order"].append("missing")
    with pytest.raises(ValidationError):
        JobSpec.model_validate(data)


def test_facts_contact_application_process_validate() -> None:
    spec = JobSpec.model_validate(_component_spec())
    assert any(c.type == "facts" for c in spec.components)
    assert any(c.type == "contact" for c in spec.components)
    assert any(c.type == "application_process" for c in spec.components)


def test_custom_class_name_and_attributes_validate() -> None:
    spec = JobSpec.model_validate(_component_spec())
    contact = [c for c in spec.components if c.type == "contact"][0]
    assert contact.class_name == "contact-card"
    assert contact.attributes["data-region"] == "dk"


def test_event_handler_attributes_are_rejected() -> None:
    data = _component_spec()
    data["components"][3]["attributes"] = {"onclick": "alert(1)"}
    with pytest.raises(ValidationError):
        JobSpec.model_validate(data)


def test_javascript_scheme_urls_are_rejected() -> None:
    data = _component_spec()
    data["components"][0]["cta"] = {"label": "Apply", "url": "javascript:alert(1)"}
    with pytest.raises(ValidationError):
        JobSpec.model_validate(data)


def test_component_markdown_render_includes_facts_and_process() -> None:
    spec = JobSpec.model_validate(_component_spec())
    output = render_jobspec(spec, format="markdown")
    assert "# Senior IT-Security Manager" in output
    assert "## Jobdetaljer" in output
    assert "## Sådan søger du" in output


def test_component_html_render_includes_cta_contact_and_order() -> None:
    spec = JobSpec.model_validate(_component_spec())
    output = render_jobspec(spec, format="html", theme="modern")
    assert "Send ansøgning" in output
    assert "Har du spørgsmål?" in output
    assert 'data-component-id="hero"' in output
    assert output.index('data-component-id="hero"') < output.index('data-component-id="facts"')


def test_component_json_render_contains_normalized_components() -> None:
    spec = JobSpec.model_validate(_component_spec())
    output = render_jobspec(spec, format="json")
    payload = json.loads(output)
    assert payload["page"]["layout"] == "job_detail"
    assert any(component["type"] == "facts" for component in payload["components"])


def test_inline_js_not_rendered_without_explicit_allow() -> None:
    spec = JobSpec.model_validate(_component_spec())
    output = render_jobspec(spec, format="html")
    assert "console.log('x')" not in output


def test_print_link_does_not_use_inline_event_handler() -> None:
    spec = JobSpec.model_validate(_component_spec())
    output = render_jobspec(spec, format="html")
    assert "onclick=" not in output


def test_inline_js_rendered_when_allow_inline_true() -> None:
    data = _component_spec()
    data["rendering"]["js"]["allow_inline"] = True
    spec = JobSpec.model_validate(data)
    output = render_jobspec(spec, format="html")
    assert "console.log('x')" in output


def test_component_render_works_for_markdown_html_json() -> None:
    spec = JobSpec.model_validate(_component_spec())
    assert "# Senior IT-Security Manager" in render_jobspec(spec, format="markdown")
    assert "<!doctype html>" in render_jobspec(spec, format="html").lower()
    assert json.loads(render_jobspec(spec, format="json"))["id"] == "danish-security-manager"


def test_danish_example_file_validates_and_renders() -> None:
    from neksus.core.jobspec.parser import load_jobspec

    example = ROOT / "examples" / "danish-job-detail.jobspec.yaml"
    spec = load_jobspec(example)
    assert "Senior IT-Security Manager" in render_jobspec(spec, format="markdown")
