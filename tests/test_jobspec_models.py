from __future__ import annotations

import pytest
from pydantic import ValidationError

from neksus.core.jobspec.models import JobSpec


def test_jobspec_model_rejects_invalid_id() -> None:
    with pytest.raises(ValidationError):
        JobSpec.model_validate(
            {
                "schema_version": 1,
                "id": "Backend Engineer",
                "page": {"layout": "job_detail"},
                "job": {"title": "Backend Engineer"},
                "components": [
                    {
                        "type": "list",
                        "id": "requirements",
                        "variant": "bullets",
                        "title": "Requirements",
                        "items": ["One"],
                    }
                ],
            }
        )


def test_jobspec_model_rejects_empty_requirements_component() -> None:
    with pytest.raises(ValidationError):
        JobSpec.model_validate(
            {
                "schema_version": 1,
                "id": "backend-engineer",
                "page": {"layout": "job_detail"},
                "job": {"title": "Backend Engineer"},
                "components": [
                    {
                        "type": "list",
                        "id": "requirements",
                        "variant": "bullets",
                        "title": "Requirements",
                        "items": [],
                    }
                ],
            }
        )


def test_jobspec_model_accepts_stitch_structural_components() -> None:
    spec = JobSpec.model_validate(
        {
            "schema_version": 1,
            "id": "stitch-shape",
            "page": {
                "layout": "job_detail",
                "component_order": [
                    "header",
                    "nav",
                    "actions",
                    "hero",
                    "chips",
                    "grid",
                    "meta",
                ],
            },
            "job": {"title": "Architect", "intro": "Intro"},
            "components": [
                {
                    "type": "header_brand",
                    "id": "header",
                    "variant": "bar",
                    "placement": "fullwidth",
                    "brand_name": "Nordwell",
                },
                {
                    "type": "nav_links",
                    "id": "nav",
                    "variant": "top",
                    "placement": "fullwidth",
                    "links": [{"label": "Jobs", "url": "https://example.com/jobs"}],
                },
                {
                    "type": "header_actions",
                    "id": "actions",
                    "variant": "buttons",
                    "placement": "fullwidth",
                    "actions": [
                        {
                            "label": "Apply",
                            "url": "https://example.com/apply",
                            "variant": "primary",
                        }
                    ],
                },
                {
                    "type": "hero",
                    "id": "hero",
                    "variant": "split",
                    "title": "Architect",
                    "intro": "Intro",
                },
                {
                    "type": "meta_chips",
                    "id": "chips",
                    "items": [{"label": "Location", "value": "Copenhagen", "icon": "PIN"}],
                },
                {
                    "type": "feature_grid",
                    "id": "grid",
                    "variant": "cards",
                    "items": [{"title": "System Design", "body": "Build robust systems"}],
                },
                {
                    "type": "meta_panel",
                    "id": "meta",
                    "placement": "sidebar",
                    "facts": [{"label": "Type", "value": "Full-time", "icon": "WORK"}],
                },
            ],
        }
    )
    assert spec.id == "stitch-shape"


def test_stitch_layout_mode_requires_region_clusters() -> None:
    with pytest.raises(ValidationError):
        JobSpec.model_validate(
            {
                "schema_version": 1,
                "id": "stitch-missing",
                "page": {
                    "layout": "job_detail",
                    "layout_mode": "stitch_job_detail",
                    "component_order": ["hero"],
                },
                "job": {"title": "Role", "intro": "Intro"},
                "components": [
                    {
                        "type": "hero",
                        "id": "hero",
                        "variant": "split",
                        "region": "hero",
                        "title": "Role",
                    }
                ],
            }
        )


def test_stitch_layout_mode_requires_meta_panel_icons() -> None:
    with pytest.raises(ValidationError):
        JobSpec.model_validate(
            {
                "schema_version": 1,
                "id": "stitch-icons",
                "page": {
                    "layout": "job_detail",
                    "layout_mode": "stitch_job_detail",
                    "component_order": [
                        "hb",
                        "nav",
                        "act",
                        "banner",
                        "hero",
                        "chips",
                        "main",
                        "grid",
                        "list",
                        "quote",
                        "benefits",
                        "process",
                        "company",
                        "legal",
                        "meta",
                        "social",
                        "map",
                    ],
                },
                "job": {"title": "Role", "intro": "Intro"},
                "components": [
                    {"type": "header_brand", "id": "hb", "region": "header", "brand_name": "N"},
                    {
                        "type": "nav_links",
                        "id": "nav",
                        "region": "header",
                        "links": [{"label": "Jobs", "url": "https://example.com"}],
                    },
                    {
                        "type": "header_actions",
                        "id": "act",
                        "region": "header",
                        "actions": [{"label": "Apply", "url": "https://example.com"}],
                    },
                    {
                        "type": "hero_banner",
                        "id": "banner",
                        "region": "hero",
                        "image_url": "/banner.png",
                    },
                    {"type": "hero", "id": "hero", "region": "hero", "title": "Role"},
                    {
                        "type": "meta_chips",
                        "id": "chips",
                        "region": "hero",
                        "items": [{"label": "L", "value": "C", "icon": "location_on"}],
                    },
                    {"type": "rich_text", "id": "main", "region": "main", "body": "Body"},
                    {
                        "type": "feature_grid",
                        "id": "grid",
                        "region": "main",
                        "items": [{"title": "T", "body": "B"}],
                    },
                    {
                        "type": "list",
                        "id": "list",
                        "region": "main",
                        "items": ["One"],
                    },
                    {"type": "quote", "id": "quote", "region": "main", "quote": "Q"},
                    {"type": "benefits", "id": "benefits", "region": "main", "items": ["B"]},
                    {"type": "application_process", "id": "process", "region": "main"},
                    {"type": "company_profile", "id": "company", "region": "main", "body": "B"},
                    {"type": "legal", "id": "legal", "region": "main", "body": "B"},
                    {
                        "type": "meta_panel",
                        "id": "meta",
                        "region": "sidebar",
                        "facts": [{"label": "Type", "value": "Full-time"}],
                    },
                    {
                        "type": "social_links",
                        "id": "social",
                        "region": "sidebar",
                        "links": [{"label": "LinkedIn", "url": "https://example.com"}],
                    },
                    {
                        "type": "location_map",
                        "id": "map",
                        "region": "sidebar",
                        "map_url": "https://maps.google.com",
                    },
                ],
            }
        )
