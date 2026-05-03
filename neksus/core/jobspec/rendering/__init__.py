"""Rendering facade for JobSpec formats."""

from __future__ import annotations

from neksus.core.errors import UnsupportedFormatError
from neksus.core.jobspec.models import JobSpec
from neksus.core.jobspec.rendering.html import render_html
from neksus.core.jobspec.rendering.json import render_json
from neksus.core.jobspec.rendering.markdown import render_markdown
from neksus.core.jobspec.rendering.options import RenderOptions, RenderSections
from neksus.core.jobspec.rendering.themes import (
    get_theme_css,
    get_theme_metadata,
    list_theme_metadata,
    list_theme_names,
)


def render_jobspec_with_options(spec: JobSpec, options: RenderOptions) -> str:
    """Render a JobSpec using normalized render options."""
    if options.format == "markdown":
        return render_markdown(spec, options)
    if options.format == "html":
        return render_html(spec, options)
    if options.format == "json":
        return render_json(spec)
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
