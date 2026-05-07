"""HTML renderer using only the shared contract + theme package pipeline."""

from __future__ import annotations

from neksus_jobspec.jobspec.rendering.options import RenderOptions
from neksus_jobspec.jobspec.rendering.theme_contract import build_theme_render_context
from neksus_jobspec.jobspec.rendering.theme_engine import render_theme, resolve_theme_package, validate_theme_package


def _render_with_theme_package(spec, options: RenderOptions) -> str:
    package = resolve_theme_package(options.theme, spec.rendering.web.template)
    contract = build_theme_render_context(spec, options)
    validate_theme_package(package, contract)
    return render_theme(package, context={"contract": contract.model_dump(mode="json")}, custom_css=options.custom_css)


def render_html(spec, options: RenderOptions) -> str:
    """Render a JobSpec into HTML."""
    return _render_with_theme_package(spec, options)
