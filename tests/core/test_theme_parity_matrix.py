from __future__ import annotations

from pathlib import Path

import yaml

from neksus_jobspec.jobspec.models import JobSpec
from neksus_jobspec.jobspec.rendering.html import render_html
from neksus_jobspec.jobspec.rendering.options import RenderOptions

ROOT = Path(__file__).resolve().parents[2]


def _full_spec() -> JobSpec:
    data = {
        "schema_version": 1,
        "id": "parity-matrix",
        "page": {"layout": "job_detail"},
        "job": {
            "title": "Platform Engineer",
            "intro": "Build reliable systems.",
            "apply": {
                "method": "external_url",
                "label": "Apply Now",
                "url": "https://example.com/apply",
            },
        },
        "components": [
            {"type": "header_brand", "id": "hb", "brand_name": "ACME"},
            {
                "type": "header_actions",
                "id": "ha",
                "actions": [{"label": "Apply", "url": "https://example.com/apply"}],
            },
            {
                "type": "hero_banner",
                "id": "hero-banner",
                "image_url": "https://example.com/map.png",
            },
            {"type": "hero", "id": "hero", "title": "Platform Engineer", "subtitle": "Copenhagen"},
            {
                "type": "meta_chips",
                "id": "chips",
                "items": [{"label": "Location", "value": "Copenhagen"}],
            },
            {
                "type": "rich_text",
                "id": "about",
                "title": "Overview",
                "body": "Build reliable systems.",
            },
            {
                "type": "feature_grid",
                "id": "resp",
                "items": [{"title": "Own services", "body": "Deliver stable APIs"}],
            },
            {"type": "list", "id": "req", "title": "Requirements", "items": ["Python"]},
            {"type": "benefits", "id": "ben", "items": ["Remote"]},
            {"type": "application_process", "id": "proc", "steps": ["Screen", "Interview"]},
            {
                "type": "contact",
                "id": "contact",
                "name": "Hiring Team",
                "email": "jobs@example.com",
            },
            {"type": "meta_panel", "id": "meta", "facts": [{"label": "Team", "value": "Platform"}]},
            {
                "type": "social_links",
                "id": "social",
                "links": [{"label": "LinkedIn", "url": "https://example.com", "icon": "share"}],
            },
            {"type": "location_map", "id": "map", "map_url": "https://example.com/map.png"},
            {"type": "footer_brand", "id": "footer", "brand_name": "ACME", "body": "ACME Footer"},
        ],
    }
    return JobSpec.model_validate(data)


def test_parity_matrix_builtin_themes_render_full_spec() -> None:
    spec = _full_spec()
    for theme in ["soft-professional", "classic", "classic-dark"]:
        html = render_html(spec, RenderOptions(format="web", theme=theme))
        assert "Platform Engineer" in html
        assert "Requirements" in html


def test_parity_matrix_custom_theme_render_full_spec() -> None:
    spec = _full_spec()
    theme_root = ROOT / "fixtures" / "themes" / "custom-basic"
    html = render_html(spec, RenderOptions(format="web", theme=str(theme_root)))
    assert "Platform Engineer" in html
    assert 'class="jobspec-page"' in html


def test_parity_matrix_minimal_valid_fixture_still_renders() -> None:
    fixture = ROOT / "fixtures" / "valid" / "minimal-valid.jobspec.yaml"
    spec = JobSpec.model_validate(yaml.safe_load(fixture.read_text(encoding="utf-8")))
    for theme in ["soft-professional", "classic", "classic-dark"]:
        html = render_html(spec, RenderOptions(format="web", theme=theme))
        assert "Backend Engineer" in html
