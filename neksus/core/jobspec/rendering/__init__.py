"""Rendering facade for JobSpec formats."""

from __future__ import annotations

from neksus.core.errors import UnsupportedFormatError
from neksus.core.jobspec.models import JobSpec
from neksus.core.jobspec.rendering.json_ld import render_json_ld
from neksus.core.jobspec.rendering.options import RenderOptions, RenderSections
from neksus.core.jobspec.rendering.themes import (
    get_theme_css,
    get_theme_metadata,
    list_theme_metadata,
    list_theme_names,
)
from neksus.core.jobspec.rendering.web import render_web


def render_jobspec_with_options(spec: JobSpec, options: RenderOptions) -> str:
    """Render a JobSpec using normalized render options."""
    if options.format == "web":
        return render_web(spec, options)
    if options.format == "json-ld":
        return render_json_ld(spec)
    raise UnsupportedFormatError(f"Unsupported render format: {options.format}")


__all__ = [
    "RenderOptions",
    "RenderSections",
    "get_theme_css",
    "get_theme_metadata",
    "list_theme_metadata",
    "list_theme_names",
    "render_jobspec_with_options",
]
