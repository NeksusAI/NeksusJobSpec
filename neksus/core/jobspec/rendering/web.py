"""Web renderer (canonical HTML source output)."""

from __future__ import annotations

from neksus.core.jobspec.rendering.html import render_html


def render_web(spec, options) -> str:
    """Render canonical web HTML."""
    return render_html(spec, options)
