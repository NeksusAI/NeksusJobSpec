"""Template helpers for generating new JobSpec files.

This module centralizes bootstrap template generation to keep `spec new`
consistent across commands.
"""

from __future__ import annotations

import re

import yaml


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


def build_jobspec_template(name: str) -> dict:
    """Build a valid default JobSpec payload from an input name."""
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


def dump_jobspec_yaml(data: dict) -> str:
    """Serialize template dictionary to YAML."""
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=False)
