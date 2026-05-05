"""Render option models."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

RenderFormat = Literal["web", "json-ld"]


class RenderSections(BaseModel):
    """Optional section visibility overrides."""

    summary: bool = True
    details: bool = True
    responsibilities: bool = True
    requirements: bool = True
    nice_to_have: bool = True


class RenderOptions(BaseModel):
    """Normalized render options for format renderers."""

    format: RenderFormat = "web"
    theme: str = "soft-professional"
    embed_css: bool = True
    custom_css: str | None = None
    asset_base_url: str | None = None
    sections: RenderSections = Field(default_factory=RenderSections)
