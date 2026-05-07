"""Pydantic models for component-based JobSpec data."""

from __future__ import annotations

import re
from datetime import date
from urllib.parse import urlparse
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

SAFE_URL_SCHEMES = {"http", "https", "mailto", "tel"}
SAFE_ATTRIBUTE_KEYS = {"id", "role", "title"}
SAFE_ATTRIBUTE_PATTERN = re.compile(r"^(data|aria)-[a-z0-9_.:-]+$")


class StrictModel(BaseModel):
    """Base model that rejects unknown fields."""

    model_config = ConfigDict(extra="forbid")


def _is_safe_url(value: str) -> bool:
    raw = value.strip()
    if not raw:
        return False
    parsed = urlparse(raw)
    if parsed.scheme:
        return parsed.scheme.lower() in SAFE_URL_SCHEMES
    if raw.startswith(("/", "./", "../", "#")):
        return True
    lowered = raw.lower()
    if lowered.startswith(("javascript:", "data:", "vbscript:")):
        return False
    return bool(raw) and all(not char.isspace() for char in raw)


class PageConfig(StrictModel):
    layout: Literal["job_detail"] = "job_detail"
    layout_mode: Literal["structured_job_detail"] | None = None
    language: str | None = None
    theme: str | None = None
    component_order: list[str] = Field(default_factory=list)


class JobApply(StrictModel):
    method: Literal["email", "external_url", "ats_url", "custom", "agent_ready"]
    label: str | None = None
    email: str | None = None
    url: str | None = None
    job_reference: str | None = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned = value.strip()
        if not cleaned or "@" not in cleaned:
            raise ValueError("email must be a valid email address")
        return cleaned

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if not _is_safe_url(value):
            raise ValueError("url must use a safe scheme or a safe relative path")
        return value

    @model_validator(mode="after")
    def validate_method_fields(self) -> JobApply:
        if self.method == "email":
            if not self.email:
                raise ValueError("apply.email is required when apply.method=email")
            return self
        if self.method in {"external_url", "ats_url", "custom"} and not self.url:
            raise ValueError(f"apply.url is required when apply.method={self.method}")
        if self.method == "agent_ready":
            if not self.url:
                raise ValueError("apply.url is required when apply.method=agent_ready")
            if not self.job_reference:
                raise ValueError("apply.job_reference is required when apply.method=agent_ready")
        return self


class JobConfig(StrictModel):
    title: str
    intro: str | None = None
    apply: JobApply | None = None


class CampaignConfig(StrictModel):
    starts_at: date | None = None
    expires_at: date | None = None
    status: Literal["draft", "active", "expired", "closed"] | None = None

    @model_validator(mode="after")
    def validate_dates(self) -> CampaignConfig:
        if self.starts_at and self.expires_at and self.expires_at < self.starts_at:
            raise ValueError("campaign.expires_at must not be before campaign.starts_at")
        return self


class WebLabels(StrictModel):
    share: str = "Share"
    print: str = "Print"
    phone: str = "Phone"
    mobile: str = "Mobile"
    email: str = "Email"
    open_map: str = "Open map"
    deadline: str = "Deadline"


class ClassicThemePalette(StrictModel):
    background: str | None = None
    text: str | None = None
    muted_text: str | None = None
    border: str | None = None
    card_background: str | None = None
    footer_background: str | None = None
    button_background: str | None = None
    button_text: str | None = None

    @field_validator("*")
    @classmethod
    def validate_color(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("color value must not be empty")
        return cleaned


class ClassicThemeConfig(StrictModel):
    content_max_width_px: int = 720
    section_gap_px: int = 64
    show_section_dividers: bool = True
    responsibilities_style: Literal["cards", "list"] = "cards"
    requirements_marker: Literal["check", "dash"] = "check"
    process_style: Literal["ordered", "bullets"] = "ordered"
    footer_style: Literal["minimal", "detailed"] = "minimal"
    palette: ClassicThemePalette = Field(default_factory=ClassicThemePalette)

    @field_validator("content_max_width_px")
    @classmethod
    def validate_content_max_width_px(cls, value: int) -> int:
        if value < 480 or value > 1400:
            raise ValueError("content_max_width_px must be between 480 and 1400")
        return value

    @field_validator("section_gap_px")
    @classmethod
    def validate_section_gap_px(cls, value: int) -> int:
        if value < 24 or value > 200:
            raise ValueError("section_gap_px must be between 24 and 200")
        return value


class RenderingCssTokens(StrictModel):
    color_primary: str | None = None
    color_background: str | None = None
    font_body: str | None = None
    font_heading: str | None = None
    border_radius: str | None = None
    spacing_scale: str | None = None


class RenderingCssConfig(StrictModel):
    files: list[str] = Field(default_factory=list)
    inline: str = ""
    tokens: RenderingCssTokens = Field(default_factory=RenderingCssTokens)


class RenderingWebConfig(StrictModel):
    template: str = "soft-professional"
    facts_position: Literal["sidebar", "topbar", "grid"] = "sidebar"
    css: RenderingCssConfig = Field(default_factory=RenderingCssConfig)
    labels: WebLabels = Field(default_factory=WebLabels)
    asset_base_url: str | None = None
    show_top_apply: bool = True
    show_share_links: bool = False
    show_print_link: bool = False
    repeat_cta: bool = False
    classic: ClassicThemeConfig = Field(default_factory=ClassicThemeConfig)

    @field_validator("template")
    @classmethod
    def validate_template(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("template must not be empty")
        if any(char in cleaned for char in ("\n", "\r", "\t")):
            raise ValueError("template must not contain control whitespace")
        return cleaned

    @field_validator("asset_base_url")
    @classmethod
    def validate_asset_base_url(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if not _is_safe_url(value):
            raise ValueError("asset_base_url must use a safe scheme or a safe relative path")
        return value


class RenderingConfig(StrictModel):
    web: RenderingWebConfig = Field(default_factory=RenderingWebConfig)


class ComponentBase(StrictModel):
    type: str
    id: str
    variant: str | None = None
    title: str | None = None
    class_name: str | None = None
    attributes: dict[str, str] = Field(default_factory=dict)
    visibility: str | None = None
    render_if: dict[str, Any] | None = None
    placement: Literal["main", "sidebar", "fullwidth"] = "main"
    region: Literal["header", "hero", "main", "sidebar", "footer"] | None = None
    container: str | None = None

    @field_validator("attributes")
    @classmethod
    def validate_attributes(cls, value: dict[str, str]) -> dict[str, str]:
        for key in value:
            lowered = key.lower()
            if lowered.startswith("on"):
                raise ValueError("event handler attributes are not allowed")
            if lowered in SAFE_ATTRIBUTE_KEYS:
                continue
            if not SAFE_ATTRIBUTE_PATTERN.match(lowered):
                raise ValueError("attributes keys must be id/role/title or start with data-/aria-")
        return value


class CtaData(StrictModel):
    label: str
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        if not _is_safe_url(value):
            raise ValueError("url must use a safe scheme or a safe relative path")
        return value


class LinkItem(StrictModel):
    label: str
    url: str
    icon: str | None = None
    active: bool = False

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        if not _is_safe_url(value):
            raise ValueError("url must use a safe scheme or a safe relative path")
        return value


class HeroComponent(ComponentBase):
    type: Literal["hero"]
    variant: Literal["default", "centered", "split"] = "default"
    title: str | None = None
    subtitle: str | None = None
    intro: str | None = None
    image: str | None = None
    cta: CtaData | None = None


class FactsItem(StrictModel):
    label: str
    value: str
    icon: str | None = None


class FactsComponent(ComponentBase):
    type: Literal["facts"]
    variant: Literal["sidebar", "topbar", "grid"] = "sidebar"
    items: list[FactsItem] = Field(min_length=1)


class RichTextComponent(ComponentBase):
    type: Literal["rich_text"]
    variant: Literal["default", "narrow", "highlighted"] = "default"
    body: str


class ListComponent(ComponentBase):
    type: Literal["list"]
    variant: Literal["bullets", "numbered", "checklist"] = "bullets"
    items: list[str] = Field(min_length=1)


class QuoteComponent(ComponentBase):
    type: Literal["quote"]
    variant: Literal["plain", "card", "pullquote"] = "plain"
    quote: str
    author: str | None = None
    author_title: str | None = None
    image: str | None = None


class BenefitsComponent(ComponentBase):
    type: Literal["benefits"]
    variant: Literal["list", "cards"] = "list"
    items: list[str | dict[str, str]] = Field(min_length=1)

    @field_validator("items")
    @classmethod
    def validate_items(cls, value: list[str | dict[str, str]]) -> list[str | dict[str, str]]:
        for item in value:
            if isinstance(item, str):
                if not item.strip():
                    raise ValueError("benefits items must not contain empty strings")
                continue
            text = item.get("text")
            if not isinstance(text, str) or not text.strip():
                raise ValueError("benefits item objects must include non-empty text")
            icon = item.get("icon")
            if icon is not None and (not isinstance(icon, str) or not icon.strip()):
                raise ValueError("benefits item icon must be a non-empty string when set")
            unknown = [key for key in item if key not in {"text", "icon"}]
            if unknown:
                unknown_csv = ", ".join(unknown)
                raise ValueError(f"benefits item has unknown keys: {unknown_csv}")
        return value


class ContactComponent(ComponentBase):
    type: Literal["contact"]
    variant: Literal["card", "compact"] = "card"
    name: str
    role: str | None = None
    phone: str | None = None
    mobile: str | None = None
    email: str | None = None


class CompanyProfileComponent(ComponentBase):
    type: Literal["company_profile"]
    variant: Literal["default", "card"] = "default"
    body: str


class LegalComponent(ComponentBase):
    type: Literal["legal"]
    variant: Literal["muted", "standard"] = "standard"
    body: str


class CtaComponent(ComponentBase):
    type: Literal["cta"]
    variant: Literal["primary", "secondary", "full_width"] = "primary"
    label: str
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        if not _is_safe_url(value):
            raise ValueError("url must use a safe scheme or a safe relative path")
        return value


class MediaComponent(ComponentBase):
    type: Literal["media"]
    variant: Literal["image", "video"] = "image"
    url: str
    alt: str | None = None
    caption: str | None = None

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        if not _is_safe_url(value):
            raise ValueError("url must use a safe scheme or a safe relative path")
        return value


class ApplicationProcessComponent(ComponentBase):
    type: Literal["application_process"]
    variant: Literal["text", "steps"] = "text"
    deadline: str | None = None
    body: str | None = None
    steps: list[str] = Field(default_factory=list)


class HeaderBrandComponent(ComponentBase):
    type: Literal["header_brand"]
    variant: Literal["simple", "bar"] = "bar"
    brand_name: str
    brand_url: str | None = None
    logo_url: str | None = None
    strapline: str | None = None

    @field_validator("brand_url", "logo_url")
    @classmethod
    def validate_optional_url(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if not _is_safe_url(value):
            raise ValueError("url must use a safe scheme or a safe relative path")
        return value


class HeroBannerComponent(ComponentBase):
    type: Literal["hero_banner"]
    variant: Literal["image", "cover"] = "cover"
    image_url: str
    alt: str | None = None
    caption: str | None = None

    @field_validator("image_url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        if not _is_safe_url(value):
            raise ValueError("url must use a safe scheme or a safe relative path")
        return value


class MetaPanelComponent(ComponentBase):
    type: Literal["meta_panel"]
    variant: Literal["card", "stacked"] = "card"
    facts: list[FactsItem] = Field(default_factory=list)
    contact_name: str | None = None
    contact_role: str | None = None
    contact_phone: str | None = None
    contact_mobile: str | None = None
    contact_email: str | None = None

    @model_validator(mode="after")
    def validate_content(self) -> MetaPanelComponent:
        has_contact = any(
            [
                self.contact_name,
                self.contact_role,
                self.contact_phone,
                self.contact_mobile,
                self.contact_email,
            ]
        )
        if not self.facts and not has_contact:
            raise ValueError("meta_panel must include at least one fact or contact field")
        return self


class SocialLinksComponent(ComponentBase):
    type: Literal["social_links"]
    variant: Literal["icons", "text"] = "icons"
    links: list[LinkItem] = Field(min_length=1)


class LocationMapComponent(ComponentBase):
    type: Literal["location_map"]
    variant: Literal["map", "compact"] = "map"
    map_url: str
    address: str | None = None
    caption: str | None = None
    embed: bool = True
    embed_height: int = 220

    @field_validator("map_url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        if not _is_safe_url(value):
            raise ValueError("url must use a safe scheme or a safe relative path")
        return value

    @field_validator("embed_height")
    @classmethod
    def validate_embed_height(cls, value: int) -> int:
        if value < 120 or value > 640:
            raise ValueError("embed_height must be between 120 and 640")
        return value


class FooterBrandComponent(ComponentBase):
    type: Literal["footer_brand"]
    variant: Literal["default", "minimal"] = "default"
    brand_name: str
    body: str
    links: list[LinkItem] = Field(default_factory=list)


class NavLinksComponent(ComponentBase):
    type: Literal["nav_links"]
    variant: Literal["top", "inline"] = "top"
    links: list[LinkItem] = Field(min_length=1)


class HeaderAction(StrictModel):
    label: str
    url: str
    variant: Literal["primary", "secondary"] = "secondary"
    size: Literal["sm", "md", "lg"] = "md"
    intent: Literal["primary", "secondary"] | None = None

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        if not _is_safe_url(value):
            raise ValueError("url must use a safe scheme or a safe relative path")
        return value


class HeaderActionsComponent(ComponentBase):
    type: Literal["header_actions"]
    variant: Literal["buttons", "links"] = "buttons"
    actions: list[HeaderAction] = Field(min_length=1)


class FeatureCard(StrictModel):
    title: str
    body: str
    icon: str | None = None


class FeatureGridComponent(ComponentBase):
    type: Literal["feature_grid"]
    variant: Literal["cards", "compact"] = "cards"
    columns_mobile: Literal[1] = 1
    columns_desktop: Literal[1, 2, 3] = 2
    items: list[FeatureCard] = Field(min_length=1)


class MetaChip(StrictModel):
    label: str
    value: str
    icon: str | None = None


class MetaChipsComponent(ComponentBase):
    type: Literal["meta_chips"]
    variant: Literal["pills", "tags"] = "pills"
    items: list[MetaChip] = Field(min_length=1)


Component = Annotated[
    HeroComponent
    | FactsComponent
    | RichTextComponent
    | ListComponent
    | QuoteComponent
    | BenefitsComponent
    | ContactComponent
    | CompanyProfileComponent
    | LegalComponent
    | CtaComponent
    | MediaComponent
    | ApplicationProcessComponent
    | HeaderBrandComponent
    | HeroBannerComponent
    | MetaPanelComponent
    | SocialLinksComponent
    | LocationMapComponent
    | FooterBrandComponent
    | NavLinksComponent
    | HeaderActionsComponent
    | FeatureGridComponent
    | MetaChipsComponent,
    Field(discriminator="type"),
]


class JobSpec(StrictModel):
    """Top-level JobSpec model for v0.3.x component composition."""

    schema_version: int = 1
    id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    page: PageConfig = Field(default_factory=PageConfig)
    job: JobConfig
    campaign: CampaignConfig | None = None
    components: list[Component] = Field(min_length=1)
    rendering: RenderingConfig = Field(default_factory=RenderingConfig)

    @model_validator(mode="after")
    def validate_composition(self) -> JobSpec:
        if self.schema_version != 1:
            raise ValueError("schema_version must be 1")

        ids = [component.id for component in self.components]
        if len(ids) != len(set(ids)):
            raise ValueError("component IDs must be unique")

        if self.page.component_order:
            ordered = self.page.component_order
            component_ids = set(ids)
            ordered_ids = set(ordered)
            if len(ordered) != len(ordered_ids):
                raise ValueError("page.component_order must not contain duplicate IDs")
            missing = [item for item in ordered if item not in component_ids]
            extras = [item for item in ids if item not in ordered_ids]
            if missing:
                missing_csv = ", ".join(missing)
                raise ValueError(
                    f"page.component_order references missing component IDs: {missing_csv}"
                )
            if extras:
                extras_csv = ", ".join(extras)
                raise ValueError(
                    f"page.component_order must include every component ID; missing in order: {extras_csv}"
                )

        if self.page.layout_mode == "structured_job_detail":

            def infer_region(component: Component) -> str:
                if component.region:
                    return component.region
                if component.type in {"footer_brand"}:
                    return "footer"
                if component.type in {"header_brand", "nav_links", "header_actions"}:
                    return "header"
                if component.type in {"hero_banner", "hero", "meta_chips"}:
                    return "hero"
                if component.type in {"meta_panel", "social_links", "location_map"}:
                    return "sidebar"
                if component.placement == "sidebar":
                    return "sidebar"
                return "main"

            required_clusters: dict[str, set[str]] = {
                "header": {"header_brand", "nav_links", "header_actions"},
                "hero": {"hero_banner", "hero", "meta_chips"},
                "main": {
                    "rich_text",
                    "feature_grid",
                    "list",
                    "quote",
                    "benefits",
                    "application_process",
                    "company_profile",
                    "legal",
                },
                "sidebar": {"meta_panel", "social_links", "location_map"},
            }

            region_by_id = {}
            for component in self.components:
                region_by_id[component.id] = infer_region(component)

            types_by_region: dict[str, set[str]] = {}
            for component in self.components:
                region = region_by_id[component.id]
                types_by_region.setdefault(region, set()).add(component.type)
                if component.type == "meta_panel":
                    if not component.facts:
                        raise ValueError(
                            "meta_panel must include facts in structured_job_detail layout mode"
                        )
                    if any(not fact.icon for fact in component.facts):
                        raise ValueError(
                            "meta_panel facts must include icon in structured_job_detail layout mode"
                        )

            missing: list[str] = []
            for region, required in required_clusters.items():
                present = types_by_region.get(region, set())
                absent = sorted(required - present)
                if absent:
                    missing.append(f"{region}: {', '.join(absent)}")
            if missing:
                raise ValueError(
                    "structured_job_detail missing required region components: "
                    + "; ".join(missing)
                )

            if self.page.component_order:
                region_rank = {"header": 0, "hero": 1, "main": 2, "sidebar": 3, "footer": 4}
                last = -1
                for component_id in self.page.component_order:
                    rank = region_rank.get(region_by_id[component_id], 99)
                    if rank < last:
                        raise ValueError(
                            "page.component_order must follow region order: header, hero, main, sidebar, footer"
                        )
                    last = rank

        return self

    def days_remaining(self, today: date | None = None) -> int | None:
        if not self.campaign or not self.campaign.expires_at:
            return None
        reference = today or date.today()
        return (self.campaign.expires_at - reference).days

    def campaign_status_payload(self, today: date | None = None) -> dict[str, Any]:
        campaign = self.campaign
        return {
            "id": self.id,
            "title": self.job.title,
            "campaign_status": campaign.status if campaign else None,
            "starts_at": campaign.starts_at.isoformat() if campaign and campaign.starts_at else None,
            "expires_at": campaign.expires_at.isoformat() if campaign and campaign.expires_at else None,
            "days_remaining": self.days_remaining(today=today),
        }

    def resolved_theme(self, default_theme: str = "soft-professional") -> str:
        if self.rendering.web.template and self.rendering.web.template.strip():
            return self.rendering.web.template.strip()
        return default_theme

    def validation_warnings(self) -> list[dict[str, str]]:
        from collections import Counter

        warnings: list[dict[str, str]] = []
        if len(self.job.title.strip()) < 5:
            warnings.append(
                {"path": "job.title", "code": "short_title", "message": "Title is very short."}
            )
        list_components = [
            component for component in self.components if isinstance(component, ListComponent)
        ]
        for component in list_components:
            counts = Counter(item.strip().lower() for item in component.items)
            if any(count > 1 for count in counts.values()):
                warnings.append(
                    {
                        "path": f"components.{component.id}",
                        "code": "duplicate_items",
                        "message": f"Duplicate items found in list component '{component.id}'.",
                    }
                )
        return warnings

    def export_payload(
        self, target: Literal["generic", "linkedin-ready"] = "generic"
    ) -> dict[str, Any]:
        from neksus_jobspec.jobspec.exports import normalized_export_payload

        payload = normalized_export_payload(self)
        if target == "generic":
            return payload
        apply = payload["apply"] if isinstance(payload["apply"], dict) else {}
        return {
            "externalJobPostingId": self.id,
            "title": self.job.title,
            "description": payload.get("description"),
            "location": payload.get("location"),
            "companyApplyUrl": apply.get("url"),
            "employmentStatus": payload.get("employment"),
            "workplaceTypes": [],
            "listedAt": self.campaign.starts_at.isoformat()
            if self.campaign and self.campaign.starts_at
            else None,
            "validThrough": self.campaign.expires_at.isoformat()
            if self.campaign and self.campaign.expires_at
            else None,
            "companyJobCode": self.id,
        }
