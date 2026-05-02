"""Rendering for JobSpec formats."""

from __future__ import annotations

import html

from neksus.core.errors import UnsupportedFormatError
from neksus.core.jobspec.models import JobSpec


def _human_location(spec: JobSpec) -> str | None:
    """Return a human-readable location label for rendering."""
    if spec.location is None:
        return None
    base = spec.location.type.capitalize()
    parts = [item for item in [spec.location.city, spec.location.country] if item]
    if parts:
        return f"{base} ({', '.join(parts)})"
    return base


def _human_employment(spec: JobSpec) -> str | None:
    """Return a human-readable employment label for rendering."""
    if spec.employment is None:
        return None
    return spec.employment.type.replace("-", " ").title()


def _render_markdown(spec: JobSpec) -> str:
    """Render a JobSpec to markdown."""
    lines: list[str] = [f"# {spec.title}", "", "## Summary", "", spec.summary]

    # Build an optional Details section only when fields are present.
    details: list[str] = []
    if spec.department:
        details.append(f"- Department: {spec.department}")
    if spec.level:
        details.append(f"- Level: {spec.level}")
    location = _human_location(spec)
    if location:
        details.append(f"- Location: {location}")
    employment = _human_employment(spec)
    if employment:
        details.append(f"- Employment: {employment}")

    if details:
        lines.extend(["", "## Details", ""])
        lines.extend(details)

    lines.extend(["", "## Responsibilities", ""])
    lines.extend(f"- {item}" for item in spec.responsibilities)

    lines.extend(["", "## Requirements", ""])
    lines.extend(f"- {item}" for item in spec.requirements)

    # Omit optional section when the list is empty.
    if spec.nice_to_have:
        lines.extend(["", "## Nice to Have", ""])
        lines.extend(f"- {item}" for item in spec.nice_to_have)

    return "\n".join(lines).strip() + "\n"


def _html_list(items: list[str]) -> str:
    """Render a list of strings into deterministic HTML list markup."""
    rendered_items = "\n".join(f"      <li>{html.escape(item)}</li>" for item in items)
    return "<ul>\n" + rendered_items + "\n    </ul>"


def _render_html(spec: JobSpec) -> str:
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
    if details_items:
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
    if spec.nice_to_have:
        nice_to_have_section = (
            "  <section>\n"
            "    <h2>Nice to Have</h2>\n"
            f"    {_html_list(spec.nice_to_have)}\n"
            "  </section>\n"
        )

    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        f"  <title>{title}</title>\n"
        "</head>\n"
        "<body>\n"
        "  <main>\n"
        f"    <h1>{title}</h1>\n"
        "    <section>\n"
        "      <h2>Summary</h2>\n"
        f"      <p>{summary}</p>\n"
        "    </section>\n"
        f"{details_section}"
        "    <section>\n"
        "      <h2>Responsibilities</h2>\n"
        f"    {_html_list(spec.responsibilities)}\n"
        "    </section>\n"
        "    <section>\n"
        "      <h2>Requirements</h2>\n"
        f"    {_html_list(spec.requirements)}\n"
        "    </section>\n"
        f"{nice_to_have_section}"
        "  </main>\n"
        "</body>\n"
        "</html>\n"
    )


def render_jobspec(spec: JobSpec, format: str = "markdown") -> str:
    """Render a JobSpec in a supported output format."""
    if format == "markdown":
        return _render_markdown(spec)
    if format == "html":
        return _render_html(spec)
    if format not in {"markdown", "html"}:
        raise UnsupportedFormatError(f"Unsupported render format: {format}")
    raise UnsupportedFormatError(f"Unsupported render format: {format}")
