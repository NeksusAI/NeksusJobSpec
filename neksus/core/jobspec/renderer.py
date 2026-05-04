"""Rendering compatibility wrapper for JobSpec formats."""

from __future__ import annotations

from neksus.core.errors import UnsupportedFormatError
from neksus.core.jobspec.models import JobSpec
from neksus.core.jobspec.rendering import RenderOptions, RenderSections, render_jobspec_with_options


def render_jobspec(
    spec: JobSpec,
    format: str = "web",
    *,
    theme: str = "soft-professional",
    embed_css: bool = True,
    custom_css: str | None = None,
    asset_base_url: str | None = None,
    sections: RenderSections | dict[str, bool] | None = None,
) -> str:
    """Render a JobSpec in a supported output format.

    This wrapper preserves the historical import and signature compatibility
    while allowing optional render customization.
    """
    if format not in {"web", "json-ld"}:
        raise UnsupportedFormatError(f"Unsupported render format: {format}")

    section_options = RenderSections()
    if sections is not None:
        section_options = (
            sections if isinstance(sections, RenderSections) else RenderSections(**sections)
        )

    options = RenderOptions(
        format=format,
        theme=theme,
        embed_css=embed_css,
        custom_css=custom_css,
        asset_base_url=asset_base_url,
        sections=section_options,
    )
    return render_jobspec_with_options(spec, options)
