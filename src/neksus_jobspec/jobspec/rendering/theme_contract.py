"""Shared contract models for package-based theme rendering."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from neksus_jobspec.jobspec.models import JobSpec
from neksus_jobspec.jobspec.rendering.normalize import normalize_jobspec_for_render
from neksus_jobspec.jobspec.rendering.options import RenderOptions

# Phase 1 lock: every theme package must declare at least these components
# in its manifest support matrix.
GLOBAL_MANDATORY_COMPONENT_TYPES: tuple[str, ...] = (
    "header_brand",
    "nav_links",
    "header_actions",
    "hero_banner",
    "hero",
    "meta_chips",
    "rich_text",
    "feature_grid",
    "list",
    "quote",
    "benefits",
    "application_process",
    "company_profile",
    "legal",
    "meta_panel",
    "social_links",
    "location_map",
)


class ThemeMandatoryState(BaseModel):
    """Presence state for global mandatory components in the current JobSpec."""

    model_config = ConfigDict(extra="forbid")

    required: list[str]
    present: list[str]
    missing: list[str]


class ThemeRenderComponent(BaseModel):
    """Ordered, declarative component payload passed to all templates."""

    model_config = ConfigDict(extra="forbid")

    id: str
    type: str
    variant: str | None = None
    region: str
    placement: str
    payload: dict[str, Any]


class ThemeRenderContext(BaseModel):
    """Canonical context contract used by built-in and custom theme packages."""

    model_config = ConfigDict(extra="forbid")

    spec_id: str
    schema_version: int
    title: str
    intro: str | None = None
    apply_label: str | None = None
    apply_url: str | None = None
    apply_method: str | None = None
    campaign_status: str | None = None
    theme: str
    asset_base_url: str | None = None
    sections: dict[str, bool]
    labels: dict[str, str]
    show_top_apply: bool = True
    show_share_links: bool = False
    show_print_link: bool = False
    repeat_cta: bool = False
    theme_config: dict[str, Any] = Field(default_factory=dict)
    mandatory: ThemeMandatoryState
    components: list[ThemeRenderComponent]
    components_by_region: dict[str, list[ThemeRenderComponent]]
    component_groups: dict[str, list[ThemeRenderComponent]]


def _infer_region(component: Any) -> str:
    if getattr(component, "region", None):
        return str(component.region)
    component_type = str(component.type)
    if component_type in {"footer_brand"}:
        return "footer"
    if component_type in {"header_brand", "nav_links", "header_actions"}:
        return "header"
    if component_type in {"hero_banner", "hero", "meta_chips"}:
        return "hero"
    if component_type in {"meta_panel", "social_links", "location_map"}:
        return "sidebar"
    if getattr(component, "placement", "main") == "sidebar":
        return "sidebar"
    return "main"


def build_theme_render_context(spec: JobSpec, options: RenderOptions) -> ThemeRenderContext:
    """Build the canonical render context from normalized JobSpec data."""
    normalized = normalize_jobspec_for_render(spec)
    declared_types = {component.type for component in normalized.components}
    required = list(GLOBAL_MANDATORY_COMPONENT_TYPES)
    present = sorted(declared_types.intersection(required))
    missing = sorted(set(required) - declared_types)

    components: list[ThemeRenderComponent] = []
    by_region: dict[str, list[ThemeRenderComponent]] = {
        "header": [],
        "hero": [],
        "main": [],
        "sidebar": [],
        "footer": [],
    }
    by_type: dict[str, list[ThemeRenderComponent]] = {}
    for component in normalized.components:
        region = _infer_region(component)
        payload = component.model_dump(mode="json")
        node = ThemeRenderComponent(
            id=component.id,
            type=component.type,
            variant=getattr(component, "variant", None),
            region=region,
            placement=getattr(component, "placement", "main"),
            payload=payload,
        )
        components.append(node)
        by_region.setdefault(region, []).append(node)
        by_type.setdefault(component.type, []).append(node)

    return ThemeRenderContext(
        spec_id=spec.id,
        schema_version=spec.schema_version,
        title=normalized.title,
        intro=normalized.intro,
        apply_label=normalized.apply_label,
        apply_url=normalized.apply_url,
        apply_method=normalized.apply_method,
        campaign_status=normalized.campaign_status,
        theme=options.theme,
        asset_base_url=options.asset_base_url or spec.rendering.web.asset_base_url,
        sections=options.sections.model_dump(),
        labels=spec.rendering.web.labels.model_dump(),
        show_top_apply=spec.rendering.web.show_top_apply,
        show_share_links=spec.rendering.web.show_share_links,
        show_print_link=spec.rendering.web.show_print_link,
        repeat_cta=spec.rendering.web.repeat_cta,
        theme_config=dict(spec.rendering.web.theme_config),
        mandatory=ThemeMandatoryState(required=required, present=present, missing=missing),
        components=components,
        components_by_region=by_region,
        component_groups=by_type,
    )
