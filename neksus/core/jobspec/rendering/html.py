"""HTML renderer."""

from __future__ import annotations

import html

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
from neksus.core.jobspec.rendering.themes import get_theme_css


def _render_attrs(class_name: str | None, attrs: dict[str, str]) -> str:
    parts: list[str] = []
    if class_name:
        parts.append(f'class="{html.escape(class_name)}"')
    for key, value in attrs.items():
        parts.append(f'{html.escape(key)}="{html.escape(value)}"')
    return (" " + " ".join(parts)) if parts else ""


def _style_block(spec, options: RenderOptions) -> str:
    if not options.embed_css:
        return ""
    css = get_theme_css(options.theme)
    css_tokens = spec.rendering.css.tokens.model_dump()
    token_lines = [
        f"  --{key.replace('_', '-')}: {value};" for key, value in css_tokens.items() if value
    ]
    token_block = ""
    if token_lines:
        token_block = ":root {\n" + "\n".join(token_lines) + "\n}\n\n"

    composed_css = spec.rendering.css.inline.strip()
    if options.custom_css:
        composed_css = f"{composed_css}\n{options.custom_css.strip()}".strip()
    merged = f"{token_block}{css}"
    if composed_css:
        merged = f"{merged}\n\n{composed_css}"
    return (
        "  <style>\n" + "\n".join(f"    {line}" for line in merged.splitlines()) + "\n  </style>\n"
    )


def _render_component(component) -> str:
    attrs = _render_attrs(component.class_name, component.attributes)
    classes = (
        f"component component--{component.type} component--{component.type}-{component.variant}"
    )
    if component.class_name:
        classes = f"{classes} {component.class_name}"
    opening = f'<section class="{html.escape(classes)}" data-component-id="{html.escape(component.id)}"{attrs}>'

    head = f"<h2>{html.escape(component.title)}</h2>" if component.title else ""

    if isinstance(component, FactsComponent):
        items = "".join(
            f"<li><strong>{html.escape(item.label)}:</strong> {html.escape(item.value)}</li>"
            for item in component.items
        )
        return f"{opening}{head}<ul>{items}</ul></section>"
    if isinstance(component, HeroComponent):
        title = f"<h2>{html.escape(component.title)}</h2>" if component.title else ""
        subtitle = f"<p>{html.escape(component.subtitle)}</p>" if component.subtitle else ""
        intro = f"<p>{html.escape(component.intro)}</p>" if component.intro else ""
        cta = ""
        if component.cta:
            cta = (
                f'<p><a class="cta-link" href="{html.escape(component.cta.url)}">'
                f"{html.escape(component.cta.label)}</a></p>"
            )
        return f"{opening}{title}{subtitle}{intro}{cta}</section>"
    if isinstance(component, RichTextComponent):
        return f"{opening}{head}<p>{html.escape(component.body)}</p></section>"
    if isinstance(component, ListComponent):
        tag = "ol" if component.variant == "numbered" else "ul"
        items = "".join(
            f"<li>{('[ ] ' if component.variant == 'checklist' else '')}{html.escape(item)}</li>"
            for item in component.items
        )
        return f"{opening}{head}<{tag}>{items}</{tag}></section>"
    if isinstance(component, QuoteComponent):
        author = ""
        if component.author:
            suffix = f", {component.author_title}" if component.author_title else ""
            author = f"<cite>{html.escape(component.author + suffix)}</cite>"
        return f"{opening}<blockquote>{html.escape(component.quote)}</blockquote>{author}</section>"
    if isinstance(component, BenefitsComponent):
        items = "".join(f"<li>{html.escape(item)}</li>" for item in component.items)
        return f"{opening}{head}<ul>{items}</ul></section>"
    if isinstance(component, ContactComponent):
        body = [f"<p><strong>{html.escape(component.name)}</strong></p>"]
        if component.role:
            body.append(f"<p>{html.escape(component.role)}</p>")
        if component.phone:
            body.append(f"<p>Phone: {html.escape(component.phone)}</p>")
        if component.mobile:
            body.append(f"<p>Mobile: {html.escape(component.mobile)}</p>")
        if component.email:
            body.append(f"<p>Email: {html.escape(component.email)}</p>")
        return f"{opening}{head}{''.join(body)}</section>"
    if isinstance(component, CompanyProfileComponent):
        return f"{opening}{head}<p>{html.escape(component.body)}</p></section>"
    if isinstance(component, LegalComponent):
        return f"{opening}{head}<p>{html.escape(component.body)}</p></section>"
    if isinstance(component, CtaComponent):
        return (
            f'{opening}{head}<p><a class="cta-link" href="{html.escape(component.url)}">'
            f"{html.escape(component.label)}</a></p></section>"
        )
    if isinstance(component, MediaComponent):
        caption = f"<p>{html.escape(component.caption)}</p>" if component.caption else ""
        return (
            f'{opening}{head}<p><a href="{html.escape(component.url)}">{html.escape(component.url)}</a></p>'
            f"{caption}</section>"
        )
    if isinstance(component, ApplicationProcessComponent):
        deadline = (
            f"<p><strong>Deadline:</strong> {html.escape(component.deadline)}</p>"
            if component.deadline
            else ""
        )
        body = f"<p>{html.escape(component.body)}</p>" if component.body else ""
        steps = ""
        if component.steps:
            steps = (
                "<ol>"
                + "".join(f"<li>{html.escape(step)}</li>" for step in component.steps)
                + "</ol>"
            )
        return f"{opening}{head}{deadline}{body}{steps}</section>"

    return f"{opening}{head}</section>"


def render_html(spec, options: RenderOptions) -> str:
    """Render a JobSpec into semantic single-file HTML."""
    normalized = normalize_jobspec_for_render(spec)
    html_settings = spec.rendering.html

    title = html.escape(normalized.title)
    intro = f"<p>{html.escape(normalized.intro)}</p>" if normalized.intro else ""

    apply = ""
    if normalized.apply_label and normalized.apply_url:
        apply = (
            f'<p><a class="cta-link" href="{html.escape(normalized.apply_url)}">'
            f"{html.escape(normalized.apply_label)}</a></p>"
        )

    share_links = ""
    if html_settings.show_share_links:
        share_links = '<p class="share-links"><a href="#">Share</a></p>'

    print_link = ""
    if html_settings.show_print_link:
        print_link = '<p class="print-link"><a href="#" onclick="window.print(); return false;">Print</a></p>'

    component_html = "\n".join(_render_component(component) for component in normalized.components)

    repeated_cta = ""
    if html_settings.repeat_cta and apply:
        repeated_cta = f'<footer class="repeat-cta">{apply}</footer>'

    js_files = "\n".join(
        f'  <script src="{html.escape(path)}"></script>' for path in spec.rendering.js.files
    )
    inline_js = ""
    if spec.rendering.js.allow_inline and spec.rendering.js.inline.strip():
        inline_js = f"  <script>\n{spec.rendering.js.inline.strip()}\n  </script>"

    layout_class = f"layout-facts-{html.escape(html_settings.facts_position)}"

    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"  <title>{title}</title>\n"
        f"{_style_block(spec, options)}"
        "</head>\n"
        f'<body class="{layout_class}">\n'
        "  <main>\n"
        f"    <h1>{title}</h1>\n"
        f"    {intro}\n"
        f"    {apply}\n"
        f"    {share_links}\n"
        f"    {print_link}\n"
        f"    {component_html}\n"
        f"    {repeated_cta}\n"
        "  </main>\n"
        f"{js_files}\n"
        f"{inline_js}\n"
        "</body>\n"
        "</html>\n"
    )
