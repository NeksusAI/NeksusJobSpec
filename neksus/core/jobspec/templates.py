"""Template helpers for generating new JobSpec files.

This module centralizes bootstrap template generation to keep `spec new`
consistent across commands.
"""

from __future__ import annotations

import re

import yaml

TEMPLATE_NAMES = ("basic", "engineering", "product", "sales")


def slugify_name(name: str) -> str:
    """Slugify a job name into a valid ID/file stem."""
    # Normalize user input into a lowercase slug-like base.
    lowered = name.strip().lower()
    replaced = re.sub(r"[^a-z0-9\s-]", "", lowered)
    hyphenated = re.sub(r"[\s_]+", "-", replaced)
    slug = re.sub(r"-+", "-", hyphenated).strip("-")
    return slug


def title_from_name(name: str) -> str:
    """Convert an input name into a human-readable title."""
    words = [word for word in re.split(r"[\s_-]+", name.strip()) if word]
    return " ".join(word.capitalize() for word in words) or "Untitled Role"


def list_template_names() -> tuple[str, ...]:
    """List stable built-in template names."""
    return TEMPLATE_NAMES


def _base_template(name: str) -> dict:
    """Build a baseline valid JobSpec payload."""
    slug = slugify_name(name)
    return {
        "schema_version": 1,
        "id": slug,
        "title": title_from_name(name),
        "department": None,
        "level": None,
        "location": {"type": "remote", "city": None, "country": None},
        "summary": "Describe the role.",
        "responsibilities": ["Define the main responsibilities."],
        "requirements": ["Define the core requirements."],
        "nice_to_have": [],
        "employment": {"type": "full-time"},
    }


def build_jobspec_template(name: str, template: str = "basic") -> dict:
    """Build a valid template payload from an input name and template name."""
    if template not in TEMPLATE_NAMES:
        raise ValueError(f"Unknown template: {template}")

    data = _base_template(name)
    if template == "basic":
        return data
    if template == "engineering":
        data["department"] = "Engineering"
        data["level"] = "Mid"
        data["summary"] = "Build and maintain reliable backend systems."
        data["responsibilities"] = [
            "Design and implement backend APIs.",
            "Collaborate with product and design on feature delivery.",
        ]
        data["requirements"] = [
            "3+ years of software engineering experience.",
            "Experience with backend services and data modeling.",
        ]
        data["nice_to_have"] = ["Experience with Python and cloud infrastructure."]
        return data
    if template == "product":
        data["department"] = "Product"
        data["level"] = "Senior"
        data["summary"] = "Lead product strategy and execution across key initiatives."
        data["responsibilities"] = [
            "Define product goals and roadmap priorities.",
            "Partner with engineering and design to ship outcomes.",
        ]
        data["requirements"] = [
            "Experience managing digital products end-to-end.",
            "Strong communication and stakeholder management skills.",
        ]
        data["nice_to_have"] = ["Experience with B2B SaaS products."]
        return data
    data["department"] = "Sales"
    data["level"] = "Mid"
    data["summary"] = "Drive revenue growth through consultative selling."
    data["responsibilities"] = [
        "Manage full sales cycle from prospecting to close.",
        "Maintain accurate pipeline and forecast updates.",
    ]
    data["requirements"] = [
        "Proven track record in quota-carrying sales roles.",
        "Strong communication and negotiation skills.",
    ]
    data["nice_to_have"] = ["Experience selling HR or recruiting technology."]
    return data


def dump_jobspec_yaml(data: dict) -> str:
    """Serialize template dictionary to YAML."""
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=False)
