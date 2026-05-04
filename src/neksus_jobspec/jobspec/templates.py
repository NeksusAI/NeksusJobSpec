"""Template helpers for generating new JobSpec files."""

from __future__ import annotations

import re

import yaml

TEMPLATE_NAMES = ("basic", "engineering", "product", "sales")


def slugify_name(name: str) -> str:
    lowered = name.strip().lower()
    replaced = re.sub(r"[^a-z0-9\s-]", "", lowered)
    hyphenated = re.sub(r"[\s_]+", "-", replaced)
    return re.sub(r"-+", "-", hyphenated).strip("-")


def title_from_name(name: str) -> str:
    words = [word for word in re.split(r"[\s_-]+", name.strip()) if word]
    return " ".join(word.capitalize() for word in words) or "Untitled Role"


def list_template_names() -> tuple[str, ...]:
    return TEMPLATE_NAMES


def _base_template(name: str) -> dict:
    slug = slugify_name(name)
    title = title_from_name(name)
    return {
        "schema_version": 1,
        "id": slug,
        "page": {
            "layout": "job_detail",
            "language": "en",
            "theme": "soft-professional",
            "component_order": ["hero", "responsibilities", "requirements"],
        },
        "job": {
            "title": title,
            "intro": "Describe the role.",
        },
        "components": [
            {
                "type": "hero",
                "id": "hero",
                "variant": "default",
                "title": title,
                "intro": "Describe the role.",
            },
            {
                "type": "list",
                "id": "responsibilities",
                "variant": "bullets",
                "title": "Responsibilities",
                "items": ["Define the main responsibilities."],
            },
            {
                "type": "list",
                "id": "requirements",
                "variant": "bullets",
                "title": "Requirements",
                "items": ["Define the core requirements."],
            },
        ],
    }


def build_jobspec_template(name: str, template: str = "basic") -> dict:
    if template not in TEMPLATE_NAMES:
        raise ValueError(f"Unknown template: {template}")

    data = _base_template(name)
    if template == "basic":
        return data

    if template == "engineering":
        data["components"].insert(
            1,
            {
                "type": "facts",
                "id": "facts",
                "variant": "sidebar",
                "title": "Job details",
                "items": [
                    {"label": "Department", "value": "Engineering"},
                    {"label": "Level", "value": "Mid"},
                ],
            },
        )
        data["page"]["component_order"] = ["hero", "facts", "responsibilities", "requirements"]
        return data

    if template == "product":
        data["components"].append(
            {
                "type": "benefits",
                "id": "benefits",
                "variant": "list",
                "title": "Benefits",
                "items": ["Strong cross-functional influence.", "High ownership scope."],
            }
        )
        data["page"]["component_order"] = [
            "hero",
            "responsibilities",
            "requirements",
            "benefits",
        ]
        return data

    data["components"].append(
        {
            "type": "cta",
            "id": "apply",
            "variant": "primary",
            "title": "Apply",
            "label": "Submit application",
            "url": "https://example.com/apply",
        }
    )
    data["page"]["component_order"] = ["hero", "responsibilities", "requirements", "apply"]
    return data


def dump_jobspec_yaml(data: dict) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=False)
