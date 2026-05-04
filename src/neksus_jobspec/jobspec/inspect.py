"""Inspect JobSpec metadata."""

from __future__ import annotations

from neksus_jobspec.jobspec.models import JobSpec
from neksus_jobspec.jobspec.rendering.normalize import normalize_jobspec_for_render
from neksus_jobspec.results import ValidationResult


def inspect_jobspec(spec: JobSpec, validation: ValidationResult) -> dict[str, object]:
    normalized = normalize_jobspec_for_render(spec)
    return {
        "id": spec.id,
        "title": normalized.title,
        "schema_version": spec.schema_version,
        "layout": spec.page.layout,
        "language": spec.page.language,
        "theme": spec.page.theme,
        "components_count": len(normalized.components),
        "valid": validation.valid,
    }
