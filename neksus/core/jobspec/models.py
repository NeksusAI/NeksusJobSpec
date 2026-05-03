"""Pydantic models for component-based JobSpec data."""

from __future__ import annotations

import re
from urllib.parse import urlparse
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator

SAFE_URL_SCHEMES = {"http", "https", "mailto", "tel"}
SAFE_ATTRIBUTE_KEYS = {"id", "role", "title"}
SAFE_ATTRIBUTE_PATTERN = re.compile(r"^(data|aria)-[a-z0-9_.:-]+$")


def _is_safe_url(value: str) -> bool:
    raw = value.strip()
    if not raw:
        return False
    parsed = urlparse(raw)
    if parsed.scheme:
        return parsed.scheme.lower() in SAFE_URL_SCHEMES
    return raw.startswith(("/", "./", "../", "#"))


class PageConfig(BaseModel):
    layout: Literal["job_detail"] = "job_detail"
    language: str | None = None
    theme: str | None = None
    component_order: list[str] = Field(default_factory=list)


class JobApply(BaseModel):
    label: str
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        if not _is_safe_url(value):
            raise ValueError("url must use a safe scheme or a safe relative path")
        return value


class JobConfig(BaseModel):
    title: str
    intro: str | None = None
    apply: JobApply | None = None


class RenderingHtmlConfig(BaseModel):
    facts_position: Literal["sidebar", "topbar", "grid"] = "sidebar"
    repeat_cta: bool = False
    show_share_links: bool = False
    show_print_link: bool = False


class RenderingCssTokens(BaseModel):
    color_primary: str | None = None
    color_background: str | None = None
    font_body: str | None = None
    font_heading: str | None = None
    border_radius: str | None = None
    spacing_scale: str | None = None


class RenderingCssConfig(BaseModel):
    files: list[str] = Field(default_factory=list)
    inline: str = ""
    tokens: RenderingCssTokens = Field(default_factory=RenderingCssTokens)


class RenderingJsConfig(BaseModel):
    files: list[str] = Field(default_factory=list)
    inline: str = ""
    allow_inline: bool = False

    @field_validator("files")
    @classmethod
    def validate_js_files(cls, value: list[str]) -> list[str]:
        for item in value:
            if not _is_safe_url(item):
                raise ValueError("JS file URLs must use safe schemes or safe relative paths")
        return value


class RenderingConfig(BaseModel):
    html: RenderingHtmlConfig = Field(default_factory=RenderingHtmlConfig)
    css: RenderingCssConfig = Field(default_factory=RenderingCssConfig)
    js: RenderingJsConfig = Field(default_factory=RenderingJsConfig)


class ComponentBase(BaseModel):
    type: str
    id: str
    variant: str | None = None
    title: str | None = None
    class_name: str | None = None
    attributes: dict[str, str] = Field(default_factory=dict)
    visibility: str | None = None
    render_if: dict[str, Any] | None = None

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


class CtaData(BaseModel):
    label: str
    url: str

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


class FactsItem(BaseModel):
    label: str
    value: str


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
    items: list[str] = Field(min_length=1)


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
    | ApplicationProcessComponent,
    Field(discriminator="type"),
]


class JobSpec(BaseModel):
    """Top-level JobSpec model for v0.2.0+ component composition."""

    schema_version: int = 1
    id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    page: PageConfig = Field(default_factory=PageConfig)
    job: JobConfig
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
            component_ids = set(ids)
            missing = [item for item in self.page.component_order if item not in component_ids]
            if missing:
                missing_csv = ", ".join(missing)
                raise ValueError(
                    f"page.component_order references missing component IDs: {missing_csv}"
                )

        return self
