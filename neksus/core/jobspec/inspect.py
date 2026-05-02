"""Inspect JobSpec metadata.

Creates normalized metadata for human and JSON CLI output.
"""

from __future__ import annotations

from neksus.core.jobspec.models import JobSpec
from neksus.core.results import ValidationResult


def _location_label(spec: JobSpec) -> str | None:
    """Return normalized location metadata label."""
    if spec.location is None:
        return None
    if spec.location.type == "remote":
        return "Remote"
    place = ", ".join(part for part in [spec.location.city, spec.location.country] if part)
    if place:
        return f"{spec.location.type.capitalize()} ({place})"
    return spec.location.type.capitalize()


def inspect_jobspec(spec: JobSpec, validation: ValidationResult) -> dict[str, object]:
    """Build normalized metadata for CLI output."""
    # Keep inspection output normalized and concise for stable JSON consumers.
    employment = spec.employment.type.replace("-", " ").title() if spec.employment else None
    return {
        "id": spec.id,
        "title": spec.title,
        "schema_version": spec.schema_version,
        "department": spec.department,
        "level": spec.level,
        "location": _location_label(spec),
        "employment": employment,
        "responsibilities_count": len(spec.responsibilities),
        "requirements_count": len(spec.requirements),
        "nice_to_have_count": len(spec.nice_to_have),
        "valid": validation.valid,
    }
