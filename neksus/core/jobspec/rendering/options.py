"""Render option models."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

RenderFormat = Literal["markdown", "html", "json"]
RenderTheme = Literal["default", "compact", "modern"]


class RenderSections(BaseModel):
    """Optional section visibility overrides."""

    summary: bool = True
    details: bool = True
    responsibilities: bool = True
    requirements: bool = True
    nice_to_have: bool = True


class RenderOptions(BaseModel):
    """Normalized render options for format renderers."""

    format: RenderFormat = "markdown"
    theme: RenderTheme = "default"
    embed_css: bool = True
    custom_css: str | None = None
    sections: RenderSections = Field(default_factory=RenderSections)
