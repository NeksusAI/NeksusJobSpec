"""Pydantic models for component-based JobSpec data."""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, model_validator


class PageConfig(BaseModel):
    layout: Literal["job_detail"] = "job_detail"
    language: str | None = None
    theme: str | None = None
    component_order: list[str] = Field(default_factory=list)


class JobApply(BaseModel):
    label: str
    url: str


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


class CtaData(BaseModel):
    label: str
    url: str


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


class MediaComponent(ComponentBase):
    type: Literal["media"]
    variant: Literal["image", "video"] = "image"
    url: str
    alt: str | None = None
    caption: str | None = None


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
