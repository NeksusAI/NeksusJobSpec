"""Normalization helpers for component-based JobSpecs."""

from __future__ import annotations

from dataclasses import dataclass

from neksus.core.jobspec.models import Component, JobSpec


@dataclass
class NormalizedJobPage:
    title: str
    intro: str | None
    apply_label: str | None
    apply_url: str | None
    components: list[Component]


def normalize_jobspec_for_render(spec: JobSpec) -> NormalizedJobPage:
    """Normalize a JobSpec into a component-oriented representation."""
    apply_label = spec.job.apply.label if spec.job.apply else None
    apply_url = spec.job.apply.url if spec.job.apply else None

    components = spec.components
    if spec.page.component_order:
        order = {
            component_id: index for index, component_id in enumerate(spec.page.component_order)
        }
        components = sorted(components, key=lambda item: order.get(item.id, len(order) + 1000))

    return NormalizedJobPage(
        title=spec.job.title,
        intro=spec.job.intro,
        apply_label=apply_label,
        apply_url=apply_url,
        components=components,
    )


def normalized_json_payload(spec: JobSpec) -> dict[str, object]:
    """Return normalized JSON payload for machine workflows."""
    normalized = normalize_jobspec_for_render(spec)
    return {
        "schema_version": spec.schema_version,
        "id": spec.id,
        "title": normalized.title,
        "page": spec.page.model_dump(),
        "job": spec.job.model_dump(),
        "components": [component.model_dump() for component in normalized.components],
        "rendering": spec.rendering.model_dump(),
    }
