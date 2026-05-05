from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from neksus_jobspec.jobspec.models import JobSpec
from neksus_jobspec.jobspec.renderer import render_jobspec

ROOT = Path(__file__).resolve().parents[1]


def _component_spec() -> dict:
    return {
        "schema_version": 1,
        "id": "danish-security-manager",
        "page": {
            "layout": "job_detail",
            "language": "da",
            "theme": "soft-professional",
            "component_order": ["header", "banner", "hero", "meta", "process", "contact"],
        },
        "job": {
            "title": "Senior IT-Security Manager",
            "intro": "Vil du være med til at styrke vores sikkerhed?",
            "apply": {
                "method": "external_url",
                "label": "Send ansøgning",
                "url": "https://example.com/apply",
            },
        },
        "components": [
            {
                "type": "header_brand",
                "id": "header",
                "variant": "bar",
                "placement": "fullwidth",
                "brand_name": "Velliv",
            },
            {
                "type": "hero_banner",
                "id": "banner",
                "variant": "cover",
                "placement": "fullwidth",
                "image_url": "/assets/banner.png",
                "alt": "Banner",
            },
            {
                "type": "hero",
                "id": "hero",
                "variant": "split",
                "title": "Senior IT-Security Manager",
                "intro": "Vil du være med til at styrke vores sikkerhed?",
            },
            {
                "type": "meta_panel",
                "id": "meta",
                "variant": "card",
                "placement": "sidebar",
                "title": "Jobdetaljer",
                "facts": [
                    {"label": "Region", "value": "Region Hovedstaden"},
                    {"label": "Jobtype", "value": "Fast"},
                ],
                "contact_name": "Anna Hansen",
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
                "placement": "sidebar",
            },
        ],
        "rendering": {
            "web": {
                "facts_position": "sidebar",
                "repeat_cta": True,
                "show_share_links": True,
                "show_print_link": True,
                "labels": {
                    "share": "Del",
                    "print": "Printvenlig version",
                    "phone": "Telefon",
                    "mobile": "Mobil",
                    "email": "E-mail",
                    "open_map": "Åbn kort",
                    "deadline": "Ansøgningsfrist",
                },
                "asset_base_url": "../assets",
                "show_top_apply": True,
                "css": {"files": [], "inline": ".job { color: black; }", "tokens": {}},
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
    assert len(spec.components) == 6


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
    assert any(c.type == "meta_panel" for c in spec.components)
    assert any(c.type == "contact" for c in spec.components)
    assert any(c.type == "application_process" for c in spec.components)


def test_custom_class_name_and_attributes_validate() -> None:
    spec = JobSpec.model_validate(_component_spec())
    contact = [c for c in spec.components if c.type == "contact"][0]
    assert contact.class_name == "contact-card"
    assert contact.attributes["data-region"] == "dk"


def test_event_handler_attributes_are_rejected() -> None:
    data = _component_spec()
    data["components"][5]["attributes"] = {"onclick": "alert(1)"}
    with pytest.raises(ValidationError):
        JobSpec.model_validate(data)


def test_javascript_scheme_urls_are_rejected() -> None:
    data = _component_spec()
    data["components"][0]["cta"] = {"label": "Apply", "url": "javascript:alert(1)"}
    with pytest.raises(ValidationError):
        JobSpec.model_validate(data)


def test_component_web_render_includes_facts_and_process() -> None:
    spec = JobSpec.model_validate(_component_spec())
    output = render_jobspec(spec, format="web")
    assert "Senior IT-Security Manager" in output
    assert "Quick Facts" in output
    assert "Requirements" in output


def test_component_html_render_includes_cta_contact_and_order() -> None:
    spec = JobSpec.model_validate(_component_spec())
    output = render_jobspec(spec, format="web", theme="soft-professional")
    assert "Send ansøgning" in output
    assert "Have Questions?" in output
    assert "max-w-[1100px]" in output
    assert "technical-border" in output


def test_fullwidth_footer_renders_after_main_layout() -> None:
    data = _component_spec()
    data["page"]["component_order"] = [
        "header",
        "banner",
        "hero",
        "meta",
        "process",
        "contact",
        "footer",
    ]
    data["components"].append(
        {
            "type": "footer_brand",
            "id": "footer",
            "variant": "default",
            "placement": "fullwidth",
            "brand_name": "Nordwell",
            "body": "Footer text",
        }
    )
    spec = JobSpec.model_validate(data)
    output = render_jobspec(spec, format="web", theme="soft-professional")
    assert "Footer text" in output
    assert output.index("Quick Facts") < output.index("Footer text")


def test_component_json_ld_render_contains_jobposting_shape() -> None:
    spec = JobSpec.model_validate(_component_spec())
    output = render_jobspec(spec, format="json-ld")
    payload = json.loads(output)
    assert payload["@type"] == "JobPosting"
    assert payload["title"] == "Senior IT-Security Manager"


def test_component_order_must_include_all_components_when_set() -> None:
    data = _component_spec()
    data["page"]["component_order"] = ["hero", "meta"]
    with pytest.raises(ValidationError):
        JobSpec.model_validate(data)


def test_structural_components_validate() -> None:
    spec = JobSpec.model_validate(_component_spec())
    assert any(c.type == "header_brand" for c in spec.components)
    assert any(c.type == "hero_banner" for c in spec.components)
    assert any(c.type == "meta_panel" for c in spec.components)


def test_inline_js_not_rendered_without_explicit_allow() -> None:
    spec = JobSpec.model_validate(_component_spec())
    output = render_jobspec(spec, format="web")
    assert "console.log('x')" not in output


def test_html_uses_configurable_labels_for_meta_and_actions() -> None:
    data = _component_spec()
    data["rendering"]["web"]["show_share_links"] = True
    data["rendering"]["web"]["show_print_link"] = True
    data["rendering"]["web"]["labels"] = {
        "share": "Del",
        "print": "Printvenlig version",
        "phone": "Telefon",
        "mobile": "Mobil",
        "email": "E-mail",
        "open_map": "Åbn kort",
        "deadline": "Ansøgningsfrist",
    }
    spec = JobSpec.model_validate(data)
    output = render_jobspec(spec, format="web")
    assert "share" in output
    assert "report" in output


def test_print_link_does_not_use_inline_event_handler() -> None:
    spec = JobSpec.model_validate(_component_spec())
    output = render_jobspec(spec, format="web")
    assert "onclick=" not in output


def test_relative_media_url_uses_asset_base_url() -> None:
    data = _component_spec()
    data["components"][1]["image_url"] = "hero.svg"
    data["rendering"]["web"]["asset_base_url"] = "../assets"
    spec = JobSpec.model_validate(data)
    output = render_jobspec(spec, format="web")
    assert 'src="hero.svg"' in output


def test_show_top_apply_false_hides_top_apply() -> None:
    data = _component_spec()
    data["rendering"]["web"]["show_top_apply"] = False
    spec = JobSpec.model_validate(data)
    output = render_jobspec(spec, format="web")
    assert "Send ansøgning" in output


def test_component_render_works_for_web_and_json_ld() -> None:
    spec = JobSpec.model_validate(_component_spec())
    assert "<!doctype html>" in render_jobspec(spec, format="web").lower()
    assert json.loads(render_jobspec(spec, format="json-ld"))["@type"] == "JobPosting"


def test_danish_example_file_validates_and_renders() -> None:
    from neksus_jobspec.jobspec.parser import load_jobspec

    example = ROOT / "examples" / "job-detail.jobspec.yaml"
    spec = load_jobspec(example)
    assert "<!doctype html>" in render_jobspec(spec, format="web").lower()
