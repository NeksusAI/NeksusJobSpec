"""HTML renderer."""

from __future__ import annotations

import html
from urllib.parse import urlparse

from neksus.core.jobspec.models import (
    ApplicationProcessComponent,
    BenefitsComponent,
    CompanyProfileComponent,
    ContactComponent,
    CtaComponent,
    FactsComponent,
    FooterBrandComponent,
    HeaderBrandComponent,
    HeroBannerComponent,
    HeroComponent,
    LegalComponent,
    ListComponent,
    LocationMapComponent,
    MediaComponent,
    MetaPanelComponent,
    QuoteComponent,
    RichTextComponent,
    SocialLinksComponent,
)
from neksus.core.jobspec.rendering.normalize import normalize_jobspec_for_render
from neksus.core.jobspec.rendering.options import RenderOptions
from neksus.core.jobspec.rendering.themes import get_theme_css


def _resolve_output_url(value: str, asset_base_url: str | None) -> str:
    if not asset_base_url:
        return value
    parsed = urlparse(value)
    if parsed.scheme or value.startswith(("/", "#")):
        return value
    base = asset_base_url.rstrip("/")
    suffix = value.lstrip("./")
    return f"{base}/{suffix}" if suffix else base


def _render_attrs(attrs: dict[str, str]) -> str:
    parts = [f'{html.escape(key)}="{html.escape(value)}"' for key, value in attrs.items()]
    return (" " + " ".join(parts)) if parts else ""


def _style_block(spec, options: RenderOptions) -> str:
    web = spec.rendering.web
    template_map = {
        "default": "default",
        "compact": "compact",
        "modern": "modern",
        "classic": "classic",
        "corporate": "classic",
        "minimal": "compact",
    }
    theme_name = template_map.get(web.template, options.theme)
    css = get_theme_css(theme_name) if options.embed_css else ""
    css_tokens = web.css.tokens.model_dump()
    token_lines = [
        f"  --{key.replace('_', '-')}: {value};" for key, value in css_tokens.items() if value
    ]
    token_block = ""
    if token_lines:
        token_block = ":root {\n" + "\n".join(token_lines) + "\n}\n\n"

    composed_css = web.css.inline.strip()
    if options.custom_css:
        composed_css = f"{composed_css}\n{options.custom_css.strip()}".strip()
    merged = f"{token_block}{css}"
    if composed_css:
        merged = f"{merged}\n\n{composed_css}"
    if not merged.strip():
        return ""
    return (
        "  <style>\n" + "\n".join(f"    {line}" for line in merged.splitlines()) + "\n  </style>\n"
    )


def _css_link_blocks(spec, asset_base_url: str | None) -> str:
    css_files = spec.rendering.web.css.files
    if not css_files:
        return ""
    blocks = []
    for css_file in css_files:
        href = _resolve_output_url(css_file, asset_base_url)
        blocks.append(f'  <link rel="stylesheet" href="{html.escape(href)}">\n')
    return "".join(blocks)


def _component_wrapper(component, inner: str) -> str:
    classes = [
        "component",
        f"component--{component.type}",
        f"component--{component.type}-{component.variant}",
        f"placement--{component.placement}",
    ]
    if component.class_name:
        classes.append(component.class_name)
    container = (
        f' data-container="{html.escape(component.container)}"' if component.container else ""
    )
    attrs = _render_attrs(component.attributes)
    return (
        f'<section class="{html.escape(" ".join(classes))}" '
        f'data-component-id="{html.escape(component.id)}"{container}{attrs}>{inner}</section>'
    )


def _render_component(component, asset_base_url: str | None, labels) -> str:
    head = f"<h2>{html.escape(component.title)}</h2>" if component.title else ""

    if isinstance(component, FactsComponent):
        items = "".join(
            f"<li><strong>{html.escape(item.label)}:</strong> {html.escape(item.value)}</li>"
            for item in component.items
        )
        return _component_wrapper(component, f"{head}<ul>{items}</ul>")
    if isinstance(component, HeroComponent):
        title = f"<h2>{html.escape(component.title)}</h2>" if component.title else ""
        subtitle = f"<p>{html.escape(component.subtitle)}</p>" if component.subtitle else ""
        intro = f"<p>{html.escape(component.intro)}</p>" if component.intro else ""
        cta = ""
        if component.cta:
            cta_url = _resolve_output_url(component.cta.url, asset_base_url)
            cta = (
                f'<p><a class="cta-link" href="{html.escape(cta_url)}">'
                f"{html.escape(component.cta.label)}</a></p>"
            )
        return _component_wrapper(component, f"{title}{subtitle}{intro}{cta}")
    if isinstance(component, RichTextComponent):
        return _component_wrapper(component, f"{head}<p>{html.escape(component.body)}</p>")
    if isinstance(component, ListComponent):
        tag = "ol" if component.variant == "numbered" else "ul"
        items = "".join(
            f"<li>{('[ ] ' if component.variant == 'checklist' else '')}{html.escape(item)}</li>"
            for item in component.items
        )
        return _component_wrapper(component, f"{head}<{tag}>{items}</{tag}>")
    if isinstance(component, QuoteComponent):
        author = ""
        if component.author:
            suffix = f", {component.author_title}" if component.author_title else ""
            author = f"<cite>{html.escape(component.author + suffix)}</cite>"
        return _component_wrapper(
            component, f"{head}<blockquote>{html.escape(component.quote)}</blockquote>{author}"
        )
    if isinstance(component, BenefitsComponent):
        items = "".join(f"<li>{html.escape(item)}</li>" for item in component.items)
        return _component_wrapper(component, f"{head}<ul>{items}</ul>")
    if isinstance(component, ContactComponent):
        body = [f"<p><strong>{html.escape(component.name)}</strong></p>"]
        if component.role:
            body.append(f"<p>{html.escape(component.role)}</p>")
        if component.phone:
            body.append(f"<p>{html.escape(labels.phone)}: {html.escape(component.phone)}</p>")
        if component.mobile:
            body.append(f"<p>{html.escape(labels.mobile)}: {html.escape(component.mobile)}</p>")
        if component.email:
            body.append(f"<p>{html.escape(labels.email)}: {html.escape(component.email)}</p>")
        return _component_wrapper(component, f"{head}{''.join(body)}")
    if isinstance(component, CompanyProfileComponent):
        return _component_wrapper(component, f"{head}<p>{html.escape(component.body)}</p>")
    if isinstance(component, LegalComponent):
        return _component_wrapper(component, f"{head}<p>{html.escape(component.body)}</p>")
    if isinstance(component, CtaComponent):
        cta_url = _resolve_output_url(component.url, asset_base_url)
        body = (
            f'<p><a class="cta-link" href="{html.escape(cta_url)}">'
            f"{html.escape(component.label)}</a></p>"
        )
        return _component_wrapper(component, f"{head}{body}")
    if isinstance(component, MediaComponent):
        caption = (
            f"<figcaption>{html.escape(component.caption)}</figcaption>"
            if component.caption
            else ""
        )
        alt = html.escape(component.alt or component.title or "Media")
        media_url = _resolve_output_url(component.url, asset_base_url)
        if component.variant == "video":
            media = (
                f'<video controls preload="metadata" src="{html.escape(media_url)}">{alt}</video>'
            )
        else:
            media = f'<img src="{html.escape(media_url)}" alt="{alt}" loading="lazy">'
        return _component_wrapper(component, f"{head}<figure>{media}{caption}</figure>")
    if isinstance(component, ApplicationProcessComponent):
        deadline = (
            f"<p><strong>{html.escape(labels.deadline)}:</strong> {html.escape(component.deadline)}</p>"
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
        return _component_wrapper(component, f"{head}{deadline}{body}{steps}")
    if isinstance(component, HeaderBrandComponent):
        logo = ""
        if component.logo_url:
            logo_url = _resolve_output_url(component.logo_url, asset_base_url)
            logo = (
                f'<img class="brand-logo" src="{html.escape(logo_url)}" '
                f'alt="{html.escape(component.brand_name)}" loading="lazy">'
            )
        name = f'<strong class="brand-name">{html.escape(component.brand_name)}</strong>'
        if component.brand_url:
            brand_url = _resolve_output_url(component.brand_url, asset_base_url)
            name = f'<a class="brand-name-link" href="{html.escape(brand_url)}">{name}</a>'
        strapline = (
            f'<p class="brand-strapline">{html.escape(component.strapline)}</p>'
            if component.strapline
            else ""
        )
        return _component_wrapper(
            component, f'{head}<div class="brand-row">{logo}{name}</div>{strapline}'
        )
    if isinstance(component, HeroBannerComponent):
        banner_alt = component.alt or component.title or "Banner"
        image_url = _resolve_output_url(component.image_url, asset_base_url)
        image = (
            f'<img src="{html.escape(image_url)}" alt="{html.escape(banner_alt)}" loading="eager">'
        )
        caption = (
            f"<figcaption>{html.escape(component.caption)}</figcaption>"
            if component.caption
            else ""
        )
        return _component_wrapper(component, f"{head}<figure>{image}{caption}</figure>")
    if isinstance(component, MetaPanelComponent):
        facts = "".join(
            f"<li><strong>{html.escape(item.label)}:</strong> {html.escape(item.value)}</li>"
            for item in component.facts
        )
        contact = []
        if component.contact_name:
            contact.append(f"<p><strong>{html.escape(component.contact_name)}</strong></p>")
        if component.contact_role:
            contact.append(f"<p>{html.escape(component.contact_role)}</p>")
        if component.contact_phone:
            contact.append(
                f"<p>{html.escape(labels.phone)}: {html.escape(component.contact_phone)}</p>"
            )
        if component.contact_mobile:
            contact.append(
                f"<p>{html.escape(labels.mobile)}: {html.escape(component.contact_mobile)}</p>"
            )
        if component.contact_email:
            contact.append(
                f"<p>{html.escape(labels.email)}: {html.escape(component.contact_email)}</p>"
            )
        facts_html = f"<ul>{facts}</ul>" if facts else ""
        return _component_wrapper(component, f"{head}{facts_html}{''.join(contact)}")
    if isinstance(component, SocialLinksComponent):
        links = "".join(
            f'<li><a href="{html.escape(_resolve_output_url(item.url, asset_base_url))}">{html.escape(item.label)}</a></li>'
            for item in component.links
        )
        return _component_wrapper(component, f"{head}<ul>{links}</ul>")
    if isinstance(component, LocationMapComponent):
        address = f"<p>{html.escape(component.address)}</p>" if component.address else ""
        caption = f"<p>{html.escape(component.caption)}</p>" if component.caption else ""
        map_url = _resolve_output_url(component.map_url, asset_base_url)
        map_link = f'<p><a href="{html.escape(map_url)}">{html.escape(labels.open_map)}</a></p>'
        return _component_wrapper(component, f"{head}{address}{caption}{map_link}")
    if isinstance(component, FooterBrandComponent):
        links = ""
        if component.links:
            links = (
                "<ul>"
                + "".join(
                    f'<li><a href="{html.escape(_resolve_output_url(item.url, asset_base_url))}">{html.escape(item.label)}</a></li>'
                    for item in component.links
                )
                + "</ul>"
            )
        body = (
            f"<h3>{html.escape(component.brand_name)}</h3>"
            f"<p>{html.escape(component.body)}</p>"
            f"{links}"
        )
        return _component_wrapper(component, f"{head}{body}")

    return _component_wrapper(component, head)


def render_html(spec, options: RenderOptions) -> str:
    """Render a JobSpec into semantic single-file HTML."""
    normalized = normalize_jobspec_for_render(spec)
    web_settings = spec.rendering.web
    labels = web_settings.labels
    asset_base_url = options.asset_base_url or web_settings.asset_base_url

    title = html.escape(normalized.title)
    intro = f"<p>{html.escape(normalized.intro)}</p>" if normalized.intro else ""

    apply = ""
    if normalized.apply_label and normalized.apply_url:
        apply_url = _resolve_output_url(normalized.apply_url, asset_base_url)
        apply = (
            f'<p><a class="cta-link" href="{html.escape(apply_url)}">'
            f"{html.escape(normalized.apply_label)}</a></p>"
        )

    share_links = ""
    if web_settings.show_share_links:
        share_links = (
            f'<p class="share-links"><button type="button" class="share-trigger" '
            f'data-action="share">{html.escape(labels.share)}</button></p>'
        )

    print_link = ""
    if web_settings.show_print_link:
        print_link = (
            f'<p class="print-link"><button type="button" class="print-trigger" '
            f'data-action="print">{html.escape(labels.print)}</button></p>'
        )

    ordered = normalized.components
    has_hero_component = any(item.type == "hero" for item in ordered)
    first_non_fullwidth = next(
        (idx for idx, component in enumerate(ordered) if component.placement != "fullwidth"),
        len(ordered),
    )
    last_non_fullwidth = next(
        (idx for idx in range(len(ordered) - 1, -1, -1) if ordered[idx].placement != "fullwidth"),
        -1,
    )
    fullwidth_pre = ordered[:first_non_fullwidth]
    middle = (
        ordered[first_non_fullwidth : last_non_fullwidth + 1] if last_non_fullwidth >= 0 else []
    )
    fullwidth_post = ordered[last_non_fullwidth + 1 :] if last_non_fullwidth >= 0 else []
    main_components = [item for item in middle if item.placement == "main"]
    sidebar_components = [item for item in middle if item.placement == "sidebar"]

    fullwidth_pre_html = "\n".join(
        _render_component(component, asset_base_url, labels) for component in fullwidth_pre
    )
    fullwidth_post_html = "\n".join(
        _render_component(component, asset_base_url, labels) for component in fullwidth_post
    )
    main_html = "\n".join(
        _render_component(component, asset_base_url, labels) for component in main_components
    )
    sidebar_html = "\n".join(
        _render_component(component, asset_base_url, labels) for component in sidebar_components
    )

    repeated_cta = ""
    if web_settings.repeat_cta and apply:
        repeated_cta = f'<footer class="repeat-cta">{apply}</footer>'

    js_files = ""
    inline_js = ""

    layout_class = f"layout-facts-{html.escape(web_settings.facts_position)}"
    top_heading = ""
    if not has_hero_component:
        top_heading = f"    <h1>{title}</h1>\n    {intro}\n"

    css_links = _css_link_blocks(spec, asset_base_url)

    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"  <title>{title}</title>\n"
        f"{css_links}"
        f"{_style_block(spec, options)}"
        "</head>\n"
        f'<body class="{layout_class}">\n'
        '  <main class="jobspec-page">\n'
        '    <section class="jobspec-fullwidth">\n'
        f"{fullwidth_pre_html}\n"
        "    </section>\n"
        f"{top_heading}"
        f"    {apply if web_settings.show_top_apply else ''}\n"
        f"    {share_links}\n"
        f"    {print_link}\n"
        '    <section class="jobspec-layout">\n'
        '      <article class="jobspec-main">\n'
        f"{main_html}\n"
        f"        {repeated_cta}\n"
        "      </article>\n"
        '      <aside class="jobspec-sidebar">\n'
        f"{sidebar_html}\n"
        "      </aside>\n"
        "    </section>\n"
        '    <section class="jobspec-fullwidth jobspec-fullwidth--post">\n'
        f"{fullwidth_post_html}\n"
        "    </section>\n"
        "  </main>\n"
        f"{js_files}\n"
        f"{inline_js}\n"
        "</body>\n"
        "</html>\n"
    )
