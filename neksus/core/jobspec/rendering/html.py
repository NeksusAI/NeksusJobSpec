"""HTML renderer."""

from __future__ import annotations

import html

from neksus.core.jobspec.models import JobSpec
from neksus.core.jobspec.rendering.options import RenderOptions
from neksus.core.jobspec.rendering.themes import get_theme_css


def _human_location(spec: JobSpec) -> str | None:
    if spec.location is None:
        return None
    base = spec.location.type.capitalize()
    parts = [item for item in [spec.location.city, spec.location.country] if item]
    if parts:
        return f"{base} ({', '.join(parts)})"
    return base


def _human_employment(spec: JobSpec) -> str | None:
    if spec.employment is None:
        return None
    return spec.employment.type.replace("-", " ").title()


def _html_list(items: list[str]) -> str:
    rendered_items = "\n".join(f"      <li>{html.escape(item)}</li>" for item in items)
    return "<ul>\n" + rendered_items + "\n    </ul>"


def _style_block(options: RenderOptions) -> str:
    if not options.embed_css:
        return ""
    css = get_theme_css(options.theme)
    if options.custom_css:
        css = f"{css}\n\n{options.custom_css.strip()}"
    return "  <style>\n" + "\n".join(f"    {line}" for line in css.splitlines()) + "\n  </style>\n"


def render_html(spec: JobSpec, options: RenderOptions) -> str:
    """Render a JobSpec into semantic single-file HTML."""
    title = html.escape(spec.title)
    summary = html.escape(spec.summary)

    details_items: list[str] = []
    if spec.department:
        details_items.append(f"<strong>Department:</strong> {html.escape(spec.department)}")
    if spec.level:
        details_items.append(f"<strong>Level:</strong> {html.escape(spec.level)}")
    location = _human_location(spec)
    if location:
        details_items.append(f"<strong>Location:</strong> {html.escape(location)}")
    employment = _human_employment(spec)
    if employment:
        details_items.append(f"<strong>Employment:</strong> {html.escape(employment)}")

    details_section = ""
    if options.sections.details and details_items:
        details_lines = "\n".join(f"      <li>{item}</li>" for item in details_items)
        details_section = (
            "  <section>\n"
            "    <h2>Details</h2>\n"
            "    <ul>\n"
            f"{details_lines}\n"
            "    </ul>\n"
            "  </section>\n"
        )

    nice_to_have_section = ""
    if options.sections.nice_to_have and spec.nice_to_have:
        nice_to_have_section = (
            "  <section>\n"
            "    <h2>Nice to Have</h2>\n"
            f"    {_html_list(spec.nice_to_have)}\n"
            "  </section>\n"
        )

    summary_section = ""
    if options.sections.summary:
        summary_section = (
            f"    <section>\n      <h2>Summary</h2>\n      <p>{summary}</p>\n    </section>\n"
        )

    responsibilities_section = ""
    if options.sections.responsibilities:
        responsibilities_section = (
            "    <section>\n"
            "      <h2>Responsibilities</h2>\n"
            f"    {_html_list(spec.responsibilities)}\n"
            "    </section>\n"
        )

    requirements_section = ""
    if options.sections.requirements:
        requirements_section = (
            "    <section>\n"
            "      <h2>Requirements</h2>\n"
            f"    {_html_list(spec.requirements)}\n"
            "    </section>\n"
        )

    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"  <title>{title}</title>\n"
        f"{_style_block(options)}"
        "</head>\n"
        "<body>\n"
        "  <main>\n"
        f"    <h1>{title}</h1>\n"
        f"{summary_section}"
        f"{details_section}"
        f"{responsibilities_section}"
        f"{requirements_section}"
        f"{nice_to_have_section}"
        "  </main>\n"
        "</body>\n"
        "</html>\n"
    )
