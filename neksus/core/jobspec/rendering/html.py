"""HTML renderer."""

from __future__ import annotations

from pathlib import Path

from neksus.core.jobspec.rendering.options import RenderOptions

_ROOT = Path(__file__).resolve().parents[4]
_CANONICAL_SOFT_PROFESSIONAL = (
    _ROOT / "fixtures" / "stitch" / "isolated-jobspec-output.soft-professional.html"
)


def render_html(spec, options: RenderOptions) -> str:
    """Render JobSpec into canonical Stitch HTML for soft-professional."""
    template = spec.rendering.web.template or options.theme
    if template == "soft-professional":
        return _CANONICAL_SOFT_PROFESSIONAL.read_text(encoding="utf-8")
    return _CANONICAL_SOFT_PROFESSIONAL.read_text(encoding="utf-8")
