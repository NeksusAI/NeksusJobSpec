"""Normalization helpers for component-based JobSpecs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from neksus_jobspec.jobspec.models import Component, JobSpec


@dataclass
class NormalizedJobPage:
    title: str
    intro: str | None
    apply_label: str | None
    apply_url: str | None
    apply_method: str | None
    campaign_status: str | None
    campaign_starts_at: date | None
    campaign_expires_at: date | None
    components: list[Component]


def _default_apply_label(method: str) -> str:
    if method == "email":
        return "Apply by email"
    if method == "ats_url":
        return "Apply in ATS"
    if method == "agent_ready":
        return "Apply manually or with an assistant"
    return "Apply now"


def normalize_apply(spec: JobSpec) -> tuple[str | None, str | None, str | None]:
    if not spec.job.apply:
        return None, None, None
    apply = spec.job.apply
    label = apply.label or _default_apply_label(apply.method)
    if apply.method == "email":
        return label, f"mailto:{apply.email}", apply.method
    return label, apply.url, apply.method


def normalize_jobspec_for_render(spec: JobSpec) -> NormalizedJobPage:
    """Normalize a JobSpec into a component-oriented representation."""
    apply_label, apply_url, apply_method = normalize_apply(spec)

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
        apply_method=apply_method,
        campaign_status=spec.campaign.status if spec.campaign else None,
        campaign_starts_at=spec.campaign.starts_at if spec.campaign else None,
        campaign_expires_at=spec.campaign.expires_at if spec.campaign else None,
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
        "campaign": spec.campaign.model_dump(mode="json") if spec.campaign else None,
        "components": [component.model_dump() for component in normalized.components],
        "rendering": spec.rendering.model_dump(),
    }
