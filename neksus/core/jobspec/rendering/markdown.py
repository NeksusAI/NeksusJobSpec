"""Markdown renderer."""

from __future__ import annotations

from neksus.core.jobspec.models import JobSpec
from neksus.core.jobspec.rendering.options import RenderOptions


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


def render_markdown(spec: JobSpec, options: RenderOptions) -> str:
    """Render a JobSpec to markdown with theme-aware spacing."""
    heading = "##" if options.theme != "compact" else "###"
    spacer = "" if options.theme == "compact" else ""

    lines: list[str] = [f"# {spec.title}"]

    if options.sections.summary:
        lines.extend(["", f"{heading} Summary", "", spec.summary])

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

    if options.sections.details and details:
        lines.extend(["", f"{heading} Details", ""])
        lines.extend(details)

    if options.sections.responsibilities:
        lines.extend(["", f"{heading} Responsibilities", ""])
        lines.extend(f"- {item}" for item in spec.responsibilities)

    if options.sections.requirements:
        lines.extend(["", f"{heading} Requirements", ""])
        lines.extend(f"- {item}" for item in spec.requirements)

    if options.sections.nice_to_have and spec.nice_to_have:
        lines.extend(["", f"{heading} Nice to Have", ""])
        lines.extend(f"- {item}" for item in spec.nice_to_have)

    if spacer:
        lines.append(spacer)
    return "\n".join(lines).strip() + "\n"
