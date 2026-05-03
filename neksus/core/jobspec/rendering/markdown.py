"""Markdown renderer."""

from __future__ import annotations

from neksus.core.jobspec.models import (
    ApplicationProcessComponent,
    BenefitsComponent,
    CompanyProfileComponent,
    ContactComponent,
    CtaComponent,
    FactsComponent,
    HeroComponent,
    LegalComponent,
    ListComponent,
    MediaComponent,
    QuoteComponent,
    RichTextComponent,
)
from neksus.core.jobspec.rendering.normalize import normalize_jobspec_for_render
from neksus.core.jobspec.rendering.options import RenderOptions


def _append_heading(lines: list[str], title: str | None, heading: str) -> None:
    if title:
        lines.extend(["", f"{heading} {title}", ""])


def render_markdown(spec, options: RenderOptions) -> str:
    """Render a JobSpec to markdown."""
    normalized = normalize_jobspec_for_render(spec)
    heading = "###" if options.theme == "compact" else "##"

    lines: list[str] = [f"# {normalized.title}"]
    if normalized.intro and options.sections.summary:
        lines.extend(["", f"{heading} Summary", "", normalized.intro])

    if normalized.apply_label and normalized.apply_url:
        lines.extend(["", f"[{normalized.apply_label}]({normalized.apply_url})"])

    for component in normalized.components:
        if isinstance(component, HeroComponent):
            if component.title and component.title != normalized.title:
                lines.extend(["", f"{heading} {component.title}"])
            if component.subtitle:
                lines.extend(["", component.subtitle])
            if component.intro and component.intro != normalized.intro:
                lines.extend(["", component.intro])
            if component.cta:
                lines.extend(["", f"[{component.cta.label}]({component.cta.url})"])
            continue

        if isinstance(component, FactsComponent):
            _append_heading(lines, component.title or "Facts", heading)
            for item in component.items:
                lines.append(f"- {item.label}: {item.value}")
            continue

        if isinstance(component, RichTextComponent):
            _append_heading(lines, component.title, heading)
            lines.append(component.body)
            continue

        if isinstance(component, ListComponent):
            _append_heading(lines, component.title, heading)
            if component.variant == "numbered":
                for index, item in enumerate(component.items, start=1):
                    lines.append(f"{index}. {item}")
            elif component.variant == "checklist":
                for item in component.items:
                    lines.append(f"- [ ] {item}")
            else:
                for item in component.items:
                    lines.append(f"- {item}")
            continue

        if isinstance(component, QuoteComponent):
            lines.extend(["", f"> {component.quote}"])
            if component.author:
                suffix = f", {component.author_title}" if component.author_title else ""
                lines.append(f"> — {component.author}{suffix}")
            continue

        if isinstance(component, BenefitsComponent):
            _append_heading(lines, component.title or "Benefits", heading)
            lines.extend(f"- {item}" for item in component.items)
            continue

        if isinstance(component, ContactComponent):
            _append_heading(lines, component.title or "Contact", heading)
            lines.append(f"- Name: {component.name}")
            if component.role:
                lines.append(f"- Role: {component.role}")
            if component.phone:
                lines.append(f"- Phone: {component.phone}")
            if component.mobile:
                lines.append(f"- Mobile: {component.mobile}")
            if component.email:
                lines.append(f"- Email: {component.email}")
            continue

        if isinstance(component, CompanyProfileComponent):
            _append_heading(lines, component.title or "Company", heading)
            lines.append(component.body)
            continue

        if isinstance(component, LegalComponent):
            _append_heading(lines, component.title or "Legal", heading)
            lines.append(component.body)
            continue

        if isinstance(component, CtaComponent):
            _append_heading(lines, component.title, heading)
            lines.append(f"[{component.label}]({component.url})")
            continue

        if isinstance(component, MediaComponent):
            _append_heading(lines, component.title, heading)
            label = component.alt or component.caption or "Media"
            lines.append(f"- {label}: {component.url}")
            continue

        if isinstance(component, ApplicationProcessComponent):
            _append_heading(lines, component.title or "Application process", heading)
            if component.deadline:
                lines.append(f"- Deadline: {component.deadline}")
            if component.body:
                lines.extend(["", component.body])
            if component.steps:
                for index, step in enumerate(component.steps, start=1):
                    lines.append(f"{index}. {step}")

    return "\n".join(lines).strip() + "\n"
