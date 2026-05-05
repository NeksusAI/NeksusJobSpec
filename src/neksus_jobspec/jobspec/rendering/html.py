"""HTML renderer."""

from __future__ import annotations

import html
from dataclasses import dataclass

from neksus_jobspec.errors import ConfigError
from neksus_jobspec.jobspec.models import (
    ApplicationProcessComponent,
    BenefitsComponent,
    ContactComponent,
    FooterBrandComponent,
    FeatureGridComponent,
    HeaderActionsComponent,
    HeaderBrandComponent,
    HeroBannerComponent,
    HeroComponent,
    ListComponent,
    LocationMapComponent,
    MetaChipsComponent,
    MetaPanelComponent,
    RichTextComponent,
)
from neksus_jobspec.jobspec.rendering.normalize import normalize_jobspec_for_render
from neksus_jobspec.jobspec.rendering.options import RenderOptions
from neksus_jobspec.jobspec.rendering.theme_engine import render_theme, resolve_theme_package

TAILWIND_CONFIG = """        tailwind.config = {
            darkMode: \"class\",
            theme: {
                extend: {
                    \"colors\": {
                        \"surface-container-high\": \"#e7e8e9\",
                        \"secondary-container\": \"#39b1fd\",
                        \"surface-variant\": \"#e1e3e4\",
                        \"surface-dim\": \"#d9dadb\",
                        \"secondary\": \"#006496\",
                        \"surface-container-low\": \"#f3f4f5\",
                        \"tertiary-container\": \"#4d4b4b\",
                        \"surface-tint\": \"#3351d1\",
                        \"on-tertiary-fixed\": \"#1c1b1b\",
                        \"on-error\": \"#ffffff\",
                        \"surface-container-lowest\": \"#ffffff\",
                        \"on-tertiary-fixed-variant\": \"#484646\",
                        \"surface-container-highest\": \"#e1e3e4\",
                        \"outline\": \"#757686\",
                        \"background\": \"#f8f9fa\",
                        \"primary\": \"#002696\",
                        \"on-background\": \"#191c1d\",
                        \"on-primary\": \"#ffffff\",
                        \"tertiary-fixed-dim\": \"#c9c6c5\",
                        \"tertiary-fixed\": \"#e6e1e1\",
                        \"primary-container\": \"#193cbe\",
                        \"inverse-on-surface\": \"#f0f1f2\",
                        \"primary-fixed-dim\": \"#b9c3ff\",
                        \"inverse-surface\": \"#2e3132\",
                        \"on-secondary-fixed\": \"#001e31\",
                        \"on-primary-fixed-variant\": \"#0f36b9\",
                        \"error\": \"#ba1a1a\",
                        \"inverse-primary\": \"#b9c3ff\",
                        \"surface-bright\": \"#f8f9fa\",
                        \"on-secondary\": \"#ffffff\",
                        \"on-primary-container\": \"#acb8ff\",
                        \"on-error-container\": \"#93000a\",
                        \"on-secondary-fixed-variant\": \"#004b72\",
                        \"on-secondary-container\": \"#004164\",
                        \"tertiary\": \"#363534\",
                        \"on-surface\": \"#191c1d\",
                        \"on-primary-fixed\": \"#001257\",
                        \"primary-fixed\": \"#dde1ff\",
                        \"on-tertiary-container\": \"#bfbbbb\",
                        \"surface\": \"#f8f9fa\",
                        \"secondary-fixed-dim\": \"#91cdff\",
                        \"surface-container\": \"#edeeef\",
                        \"outline-variant\": \"#c5c5d6\",
                        \"on-tertiary\": \"#ffffff\",
                        \"on-surface-variant\": \"#444654\",
                        \"secondary-fixed\": \"#cce5ff\",
                        \"error-container\": \"#ffdad6\"
                    },
                    \"borderRadius\": {
                        \"DEFAULT\": \"0.125rem\",
                        \"lg\": \"0.25rem\",
                        \"xl\": \"0.5rem\",
                        \"full\": \"0.75rem\"
                    },
                    \"spacing\": {
                        \"base\": \"8px\",
                        \"xl\": \"80px\",
                        \"md\": \"24px\",
                        \"xs\": \"4px\",
                        \"lg\": \"48px\",
                        \"gutter\": \"24px\",
                        \"content-max\": \"720px\",
                        \"sm\": \"12px\",
                        \"container-max\": \"1100px\"
                    },
                    \"fontFamily\": {
                        \"body-md\": [\"Inter\"],
                        \"h1\": [\"Inter\"],
                        \"body-lg\": [\"Inter\"],
                        \"h2\": [\"Inter\"],
                        \"display\": [\"Inter\"],
                        \"label-sm\": [\"Inter\"]
                    },
                    \"fontSize\": {
                        \"body-md\": [\"16px\", {\"lineHeight\": \"1.6\", \"fontWeight\": \"400\"}],
                        \"h1\": [\"32px\", {\"lineHeight\": \"1.2\", \"fontWeight\": \"600\"}],
                        \"body-lg\": [\"18px\", {\"lineHeight\": \"1.6\", \"fontWeight\": \"400\"}],
                        \"h2\": [\"24px\", {\"lineHeight\": \"1.3\", \"fontWeight\": \"600\"}],
                        \"display\": [\"48px\", {\"lineHeight\": \"1.1\", \"letterSpacing\": \"-0.02em\", \"fontWeight\": \"700\"}],
                        \"label-sm\": [\"12px\", {\"lineHeight\": \"1\", \"letterSpacing\": \"0.05em\", \"fontWeight\": \"600\"}]
                    }
                },
            },
        }
"""

BASE_STYLE = """        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        .technical-border { border: 1px solid #e1e3e4; }
        .custom-bullet { width: 6px; height: 6px; border-radius: 1px; background-color: #002696; display: inline-block; margin-right: 12px; margin-bottom: 2px; }
"""


@dataclass
class SoftProfessionalData:
    title: str
    location: str
    data_location: str
    salary: str
    employment: str
    apply_label: str
    campaign_notice: str | None
    about_title: str
    about_body: str
    responsibilities_title: str
    responsibility_cards: list[tuple[str, str, str]]
    requirements_title: str
    requirements: list[str]
    quick_facts: list[tuple[str, str]]
    benefits_title: str
    benefits: list[str]
    map_image: str
    map_alt: str
    map_label: str
    cta_title: str
    cta_body: str
    cta_label: str
    footer_brand: str
    footer_icons: list[str]


@dataclass
class ClassicData:
    brand_name: str
    top_action_label: str
    title: str
    subtitle: str
    apply_label: str
    overview_body: str
    responsibilities: list[tuple[str, str, str]]
    requirements: list[str]
    benefits: list[str]
    process_body: str
    process_steps: list[str]
    contact_lines: list[str]
    footer_text: str


def _escape(value: str) -> str:
    return html.escape(value, quote=True)


def _component_by_type(components, kind: str):
    for item in components:
        if item.type == kind:
            return item
    return None


def _to_soft_professional_data(spec) -> SoftProfessionalData:
    normalized = normalize_jobspec_for_render(spec)
    components = normalized.components

    hero = _component_by_type(components, "hero")
    chips = _component_by_type(components, "meta_chips")
    about = _component_by_type(components, "rich_text")
    grid = _component_by_type(components, "feature_grid")
    req = _component_by_type(components, "list")
    meta = _component_by_type(components, "meta_panel")
    benefits = _component_by_type(components, "benefits")
    banner = _component_by_type(components, "hero_banner")
    location_map = _component_by_type(components, "location_map")
    footer_brand_component = _component_by_type(components, "footer_brand")
    footer_social = _component_by_type(components, "social_links")

    title = hero.title if isinstance(hero, HeroComponent) and hero.title else normalized.title
    apply_label = normalized.apply_label or "Apply"
    campaign_notice: str | None = None
    if normalized.campaign_status == "closed":
        campaign_notice = "This position is closed."
    elif normalized.campaign_status == "expired":
        campaign_notice = "This job campaign has expired."

    location = ""
    salary = ""
    employment = ""
    if isinstance(chips, MetaChipsComponent):
        for item in chips.items:
            label = item.label.lower()
            if "location" in label:
                location = item.value
            elif "salary" in label or "comp" in label:
                salary = item.value
            elif "type" in label or "employment" in label:
                employment = item.value

    about_title = "About"
    about_body = ""
    if isinstance(about, RichTextComponent):
        about_title = about.title or about_title
        about_body = about.body

    responsibilities_title = "Responsibilities"
    responsibility_cards: list[tuple[str, str, str]] = []
    if isinstance(grid, FeatureGridComponent):
        responsibilities_title = grid.title or responsibilities_title
        for item in grid.items:
            responsibility_cards.append((item.icon or "work", item.title, item.body))

    requirements_title = "Requirements"
    requirements: list[str] = []
    if isinstance(req, ListComponent):
        requirements_title = req.title or requirements_title
        requirements = list(req.items)

    quick_facts: list[tuple[str, str]] = []
    if isinstance(meta, MetaPanelComponent):
        quick_facts = [(item.label, item.value) for item in meta.facts]

    benefits_title = "Benefits"
    benefits_tags: list[str] = []
    if isinstance(benefits, BenefitsComponent):
        benefits_title = benefits.title or benefits_title
        tags: list[str] = []
        for item in benefits.items:
            if isinstance(item, str):
                tags.append(item)
            else:
                tags.append(item.get("text", ""))
        benefits_tags = [item for item in tags if item]

    map_image = ""
    map_alt = "Map"
    if isinstance(banner, HeroBannerComponent):
        map_image = banner.image_url
        if banner.alt:
            map_alt = banner.alt
    elif isinstance(location_map, LocationMapComponent):
        map_image = location_map.map_url

    map_label = ""
    if isinstance(location_map, LocationMapComponent) and location_map.address:
        map_label = f"Main HQ: {location_map.address}"
    cta_title = "Have Questions?"
    cta_body = ""
    cta_label = "Contact"
    if isinstance(meta, MetaPanelComponent):
        if meta.contact_email:
            cta_body = meta.contact_email
    footer_brand = normalized.title
    if footer_brand_component and getattr(footer_brand_component, "body", ""):
        footer_brand = footer_brand_component.body
    footer_icons: list[str] = []
    if footer_social and getattr(footer_social, "links", None):
        icons = [item.icon for item in footer_social.links if item.icon]
        if icons:
            footer_icons = icons[:2]
    web_config = getattr(spec.rendering, "web", None)
    if web_config:
        if web_config.show_share_links and "share" not in footer_icons:
            footer_icons.append("share")
        if web_config.show_print_link and "report" not in footer_icons:
            footer_icons.append("report")

    return SoftProfessionalData(
        title=title,
        location=location,
        data_location=location.split(",")[0].strip() if "," in location else location,
        salary=salary,
        employment=employment,
        apply_label=apply_label,
        campaign_notice=campaign_notice,
        about_title=about_title,
        about_body=about_body,
        responsibilities_title=responsibilities_title,
        responsibility_cards=responsibility_cards,
        requirements_title=requirements_title,
        requirements=requirements,
        quick_facts=quick_facts,
        benefits_title=benefits_title,
        benefits=benefits_tags,
        map_image=map_image,
        map_alt=map_alt,
        map_label=map_label,
        cta_title=cta_title,
        cta_body=cta_body,
        cta_label=cta_label,
        footer_brand=footer_brand,
        footer_icons=footer_icons,
    )


def _render_soft_professional_web(spec, options: RenderOptions) -> str:
    data = _to_soft_professional_data(spec)

    cards = data.responsibility_cards
    card_html = []
    for idx, (icon, title, body) in enumerate(cards[:3]):
        col_class = " md:col-span-2" if idx == 2 else ""
        card_html.append(
            f'<div class="p-md bg-surface-container-lowest technical-border rounded-lg{col_class}">\n'
            f'<span class="material-symbols-outlined text-primary mb-sm block" data-icon="{_escape(icon)}">{_escape(icon)}</span>\n'
            f'<h3 class="font-semibold text-lg mb-xs">{_escape(title)}</h3>\n'
            f'<p class="text-sm text-on-surface-variant">{_escape(body)}</p>\n'
            "</div>"
        )

    req_html = "\n".join(
        f'<li class="flex items-start">\n<span class="custom-bullet mt-2"></span>\n<span class="font-body-md text-body-md text-on-surface-variant">{_escape(item)}</span>\n</li>'
        for item in data.requirements
    )

    facts_html = "\n".join(
        f'<div class="flex justify-between items-center">\n<span class="text-sm font-medium text-on-surface-variant">{_escape(k)}</span>\n<span class="text-sm font-bold">{_escape(v)}</span>\n</div>'
        for k, v in data.quick_facts
    )

    benefits_html = "\n".join(
        f'<span class="bg-surface-container-low text-primary text-[10px] font-bold px-2 py-1 rounded uppercase">{_escape(item)}</span>'
        for item in data.benefits
    )

    extra_css = ""
    if options.custom_css:
        extra_css = f"\n{options.custom_css.strip()}\n"

    footer_icons_html = "\n".join(
        f'<span class="material-symbols-outlined text-sm" data-icon="{_escape(icon)}">{_escape(icon)}</span>'
        for icon in data.footer_icons
    )
    campaign_notice_html = ""
    if data.campaign_notice:
        campaign_notice_html = (
            '<div class="bg-error-container text-on-error-container technical-border rounded p-sm mt-sm">'
            f"{_escape(data.campaign_notice)}</div>"
        )

    return (
        "<!DOCTYPE html>\n\n"
        '<html class="light" lang="en"><head>\n'
        '<meta charset="utf-8"/>\n'
        '<meta content="width=device-width, initial-scale=1.0" name="viewport"/>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&amp;display=swap" rel="stylesheet"/>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>\n'
        '<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>\n'
        '<script id="tailwind-config">\n'
        f"{TAILWIND_CONFIG}"
        "    </script>\n"
        "<style>\n"
        f"{BASE_STYLE}"
        f"{extra_css}"
        "    </style>\n"
        "</head>\n"
        '<body class="bg-surface-container-low font-body-md text-on-surface">\n'
        "<!-- Standalone Container -->\n"
        '<div class="max-w-[1100px] mx-auto min-h-screen bg-surface-container-low">\n'
        "<!-- Job Hero Section -->\n"
        '<header class="bg-surface-container-lowest py-lg px-md technical-border border-t-0 border-x-0">\n'
        '<div class="max-w-[1100px] mx-auto flex flex-col md:flex-row items-start md:items-center gap-md">\n'
        '<div class="w-16 h-16 bg-primary flex items-center justify-center rounded-lg shadow-sm">\n'
        '<span class="material-symbols-outlined text-on-primary text-3xl" data-icon="terminal">terminal</span>\n'
        "</div>\n"
        '<div class="flex-grow">\n'
        f'<h1 class="font-h1 text-h1 text-on-surface mb-xs">{_escape(data.title)}</h1>\n'
        f"{campaign_notice_html}\n"
        '<div class="flex flex-wrap gap-sm items-center">\n'
        '<div class="flex items-center bg-surface-container-high px-3 py-1 rounded">\n'
        '<span class="material-symbols-outlined text-sm mr-2" data-icon="location_on">location_on</span>\n'
        f'<span class="font-label-sm text-label-sm uppercase">{_escape(data.location)}</span>\n'
        "</div>\n"
        '<div class="flex items-center bg-surface-container-high px-3 py-1 rounded">\n'
        '<span class="material-symbols-outlined text-sm mr-2" data-icon="payments">payments</span>\n'
        f'<span class="font-label-sm text-label-sm uppercase">{_escape(data.salary)}</span>\n'
        "</div>\n"
        '<div class="flex items-center bg-surface-container-high px-3 py-1 rounded">\n'
        '<span class="material-symbols-outlined text-sm mr-2" data-icon="work">work</span>\n'
        f'<span class="font-label-sm text-label-sm uppercase">{_escape(data.employment)}</span>\n'
        "</div>\n"
        "</div>\n"
        "</div>\n"
        '<div class="flex gap-sm">\n'
        f'<button class="bg-primary text-on-primary px-6 py-3 font-semibold rounded hover:bg-primary-container transition-colors{" opacity-70" if data.campaign_notice else ""}">{_escape(data.apply_label)}</button>\n'
        '<button class="border border-primary text-primary px-4 py-3 font-semibold rounded hover:bg-primary hover:text-on-primary transition-colors">\n'
        '<span class="material-symbols-outlined" data-icon="bookmark">bookmark</span>\n'
        "</button>\n"
        "</div>\n"
        "</div>\n"
        "</header>\n"
        "<!-- Main Content Grid -->\n"
        '<main class="max-w-[1100px] mx-auto px-md py-xl grid grid-cols-1 lg:grid-cols-12 gap-lg">\n'
        "<!-- Left Column: Primary Details (720px equivalent constraint) -->\n"
        '<div class="lg:col-span-8 flex flex-col gap-xl">\n'
        "<!-- About the Role -->\n"
        "<section>\n"
        f'<h2 class="font-h2 text-h2 text-on-surface mb-md">{_escape(data.about_title)}</h2>\n'
        '<p class="font-body-md text-body-md text-on-surface-variant max-w-[720px]">\n'
        f"                        {_escape(data.about_body)}\n"
        "                    </p>\n"
        "</section>\n"
        "<!-- Key Responsibilities (Asymmetric Grid) -->\n"
        "<section>\n"
        f'<h2 class="font-h2 text-h2 text-on-surface mb-md">{_escape(data.responsibilities_title)}</h2>\n'
        '<div class="grid grid-cols-1 md:grid-cols-2 gap-md">\n'
        f"{chr(10).join(card_html)}\n"
        "</div>\n"
        "</section>\n"
        "<!-- Requirements (Framework Style List) -->\n"
        "<section>\n"
        f'<h2 class="font-h2 text-h2 text-on-surface mb-md">{_escape(data.requirements_title)}</h2>\n'
        '<ul class="space-y-sm">\n'
        f"{req_html}\n"
        "</ul>\n"
        "</section>\n"
        "</div>\n"
        "<!-- Right Column: Sidebar -->\n"
        '<aside class="lg:col-span-4 flex flex-col gap-md">\n'
        "<!-- Quick Facts -->\n"
        '<div class="p-md bg-surface-container-highest technical-border rounded-lg">\n'
        '<h3 class="font-label-sm text-label-sm uppercase text-on-surface-variant mb-md border-b border-surface-dim pb-sm">Quick Facts</h3>\n'
        '<div class="space-y-md">\n'
        f"{facts_html}\n"
        "</div>\n"
        "</div>\n"
        "<!-- Benefits Card -->\n"
        '<div class="p-md bg-surface-container-lowest technical-border rounded-lg">\n'
        f'<h3 class="font-label-sm text-label-sm uppercase text-on-surface-variant mb-md">{_escape(data.benefits_title)}</h3>\n'
        '<div class="flex flex-wrap gap-xs">\n'
        f"{benefits_html}\n"
        "</div>\n"
        "</div>\n"
        "<!-- Location Map Component -->\n"
        '<div class="technical-border rounded-lg overflow-hidden">\n'
        '<div class="h-48 bg-surface-variant relative">\n'
        f'<img class="w-full h-full object-cover grayscale opacity-60" data-alt="{_escape(data.map_alt)}" data-location="{_escape(data.data_location)}" src="{_escape(data.map_image)}"/>\n'
        '<div class="absolute inset-0 flex items-center justify-center">\n'
        '<div class="w-8 h-8 bg-primary rounded-full flex items-center justify-center border-2 border-white shadow-lg">\n'
        '<span class="material-symbols-outlined text-white text-sm" data-icon="location_on">location_on</span>\n'
        "</div>\n"
        "</div>\n"
        "</div>\n"
        '<div class="p-3 bg-surface-container-lowest">\n'
        f'<p class="text-xs font-bold text-on-surface">{_escape(data.map_label)}</p>\n'
        "</div>\n"
        "</div>\n"
        "<!-- Bottom Sidebar CTA -->\n"
        '<div class="p-md bg-primary rounded-lg text-on-primary">\n'
        f'<h4 class="font-bold mb-2">{_escape(data.cta_title)}</h4>\n'
        f'<p class="text-xs mb-4 opacity-90">{_escape(data.cta_body)}</p>\n'
        f'<button class="w-full bg-on-primary text-primary py-2 text-xs font-bold rounded hover:bg-secondary-container transition-colors">{_escape(data.cta_label)}</button>\n'
        "</div>\n"
        "</aside>\n"
        "</main>\n"
        "<!-- Container Footer/End State -->\n"
        '<footer class="py-md px-md border-t border-surface-variant mt-lg flex justify-between items-center opacity-60">\n'
        f'<span class="text-xs font-label-sm uppercase tracking-widest">{_escape(data.footer_brand)}</span>\n'
        '<div class="flex gap-md">\n'
        f"{footer_icons_html}\n"
        "</div>\n"
        "</footer>\n"
        "</div>\n"
        "</body></html>"
    )


def _to_classic_data(spec) -> ClassicData:
    normalized = normalize_jobspec_for_render(spec)
    components = normalized.components
    hero = _component_by_type(components, "hero")
    chips = _component_by_type(components, "meta_chips")
    about = _component_by_type(components, "rich_text")
    grid = _component_by_type(components, "feature_grid")
    req = _component_by_type(components, "list")
    benefits = _component_by_type(components, "benefits")
    process = _component_by_type(components, "application_process")
    contact = _component_by_type(components, "contact")
    meta = _component_by_type(components, "meta_panel")
    header_brand = _component_by_type(components, "header_brand")
    header_actions = _component_by_type(components, "header_actions")
    footer_brand = _component_by_type(components, "footer_brand")

    title = hero.title if isinstance(hero, HeroComponent) and hero.title else normalized.title
    subtitle = ""
    if isinstance(hero, HeroComponent) and hero.subtitle:
        subtitle = hero.subtitle
    elif isinstance(chips, MetaChipsComponent):
        subtitle = " · ".join(item.value for item in chips.items[:3])

    responsibilities: list[tuple[str, str, str]] = []
    if isinstance(grid, FeatureGridComponent):
        responsibilities = [(item.icon or "hub", item.title, item.body) for item in grid.items]

    requirements = list(req.items) if isinstance(req, ListComponent) else []

    benefit_values: list[str] = []
    if isinstance(benefits, BenefitsComponent):
        for item in benefits.items:
            benefit_values.append(item if isinstance(item, str) else item.get("text", ""))
        benefit_values = [value for value in benefit_values if value]

    process_body = ""
    process_steps: list[str] = []
    if isinstance(process, ApplicationProcessComponent):
        process_body = process.body or ""
        process_steps = list(process.steps)

    contact_lines: list[str] = []
    if isinstance(contact, ContactComponent):
        for value in [contact.name, contact.role, contact.phone, contact.mobile, contact.email]:
            if value:
                contact_lines.append(value)
    elif isinstance(meta, MetaPanelComponent):
        for value in [
            meta.contact_name,
            meta.contact_role,
            meta.contact_phone,
            meta.contact_mobile,
            meta.contact_email,
        ]:
            if value:
                contact_lines.append(value)

    brand_name = "NeksusJobSpec"
    if isinstance(header_brand, HeaderBrandComponent):
        brand_name = header_brand.brand_name

    top_action_label = normalized.apply_label or "Apply Now"
    if isinstance(header_actions, HeaderActionsComponent) and header_actions.actions:
        top_action_label = header_actions.actions[0].label

    footer_text = f"{brand_name} • {_escape(title)}"
    if isinstance(footer_brand, FooterBrandComponent):
        footer_text = footer_brand.body

    return ClassicData(
        brand_name=brand_name,
        top_action_label=top_action_label,
        title=title,
        subtitle=subtitle,
        apply_label=normalized.apply_label or "Apply Now",
        overview_body=(
            about.body if isinstance(about, RichTextComponent) else (normalized.intro or "")
        ),
        responsibilities=responsibilities,
        requirements=requirements,
        benefits=benefit_values,
        process_body=process_body,
        process_steps=process_steps,
        contact_lines=contact_lines,
        footer_text=footer_text,
    )


def _render_classic_section(title: str, body: str) -> str:
    return (
        '<section class="mb-16 border-t pt-4">'
        f'<h2 class="mb-6 text-[12px] font-bold uppercase tracking-[0.05em] text-[#444748]">{_escape(title)}</h2>'
        f'<p class="text-[18px] leading-[1.6] text-[#191c1e]">{_escape(body)}</p>'
        "</section>"
    )


def _render_classic_web(spec, options: RenderOptions, *, dark: bool) -> str:
    data = _to_classic_data(spec)
    extra_css = ""
    if options.custom_css:
        extra_css = f"\n{options.custom_css.strip()}\n"
    classic_config = spec.rendering.web.classic
    palette = classic_config.palette
    html_class = "dark" if dark else "light"
    body_bg = palette.background or ("#141313" if dark else "#f8f9fb")
    text_color = palette.text or ("#e5e2e1" if dark else "#191c1e")
    muted_color = palette.muted_text or ("#c4c7c8" if dark else "#444748")
    border_color = palette.border or ("#444748" if dark else "#c4c7c7")
    card_bg = palette.card_background or ("#1c1b1b" if dark else "#f2f4f6")
    footer_bg = palette.footer_background or ("#0e0e0e" if dark else "#ffffff")
    button_bg = palette.button_background or "#000000"
    button_text = palette.button_text or "#ffffff"
    max_width_px = classic_config.content_max_width_px
    section_gap_px = classic_config.section_gap_px
    process_container_tag = "ol" if classic_config.process_style == "ordered" else "ul"
    process_item_class = "mb-2" if classic_config.process_style == "ordered" else "mb-2 list-disc"
    requirements_icon = "check" if classic_config.requirements_marker == "check" else "remove"
    divider_style = (
        f'border-t pt-4" style="border-color:{border_color};'
        if classic_config.show_section_dividers
        else f'pt-4" style="border-color:{border_color};'
    )
    footer_text = (
        data.footer_text
        if classic_config.footer_style == "minimal"
        else f"{data.brand_name} · {data.title}"
    )

    responsibilities_html = ""
    if data.responsibilities:
        if classic_config.responsibilities_style == "cards":
            cards = []
            for icon, title, body in data.responsibilities:
                cards.append(
                    f'<div class="rounded-lg border p-6" style="border-color:{border_color};background:{card_bg};">'
                    f'<span class="material-symbols-outlined mb-4 block text-[20px]" style="color:{text_color};">{_escape(icon)}</span>'
                    f'<h3 class="mb-2 text-[18px] font-semibold" style="color:{text_color};">{_escape(title)}</h3>'
                    f'<p class="text-[16px] leading-[1.6]" style="color:{muted_color};">{_escape(body)}</p>'
                    "</div>"
                )
            body_html = (
                '<div class="grid grid-cols-1 gap-6 md:grid-cols-2">' + "".join(cards) + "</div>"
            )
        else:
            items = "".join(
                f'<li class="mb-4"><p class="mb-1 text-[18px] font-semibold" style="color:{text_color};">{_escape(title)}</p><p class="text-[16px] leading-[1.6]" style="color:{muted_color};">{_escape(body)}</p></li>'
                for _, title, body in data.responsibilities
            )
            body_html = f'<ul class="m-0 list-none p-0">{items}</ul>'
        responsibilities_html = (
            f'<section class="mb-16 {divider_style}">'
            f'<h2 class="mb-6 text-[12px] font-bold uppercase tracking-[0.05em]" style="color:{muted_color};">Responsibilities</h2>'
            + body_html
            + "</section>"
        )

    requirements_html = ""
    if data.requirements:
        requirements_html = (
            f'<section class="mb-16 {divider_style}">'
            f'<h2 class="mb-6 text-[12px] font-bold uppercase tracking-[0.05em]" style="color:{muted_color};">Requirements</h2>'
            + "".join(
                f'<div class="mb-3 flex items-start gap-3"><span class="material-symbols-outlined mt-[2px] text-[16px]" style="color:{text_color};">{requirements_icon}</span><p class="m-0" style="color:{muted_color};">{_escape(item)}</p></div>'
                for item in data.requirements
            )
            + "</section>"
        )

    benefits_html = ""
    if data.benefits:
        benefits_html = (
            f'<section class="mb-16 {divider_style}">'
            f'<h2 class="mb-6 text-[12px] font-bold uppercase tracking-[0.05em]" style="color:{muted_color};">Benefits</h2>'
            '<div class="grid grid-cols-1 md:grid-cols-2 gap-3">'
            + "".join(
                f'<div class="rounded-lg border px-4 py-3" style="border-color:{border_color};background:{card_bg};color:{text_color};">{_escape(item)}</div>'
                for item in data.benefits
            )
            + "</div></section>"
        )

    process_html = ""
    if data.process_body or data.process_steps:
        process_html = (
            f'<section class="mb-16 {divider_style}">'
            f'<h2 class="mb-6 text-[12px] font-bold uppercase tracking-[0.05em]" style="color:{muted_color};">Application Process</h2>'
            + (
                f'<p class="mb-4 text-[16px] leading-[1.6]" style="color:{text_color};">{_escape(data.process_body)}</p>'
                if data.process_body
                else ""
            )
            + (
                f'<{process_container_tag} class="pl-5 m-0">'
                + "".join(
                    f'<li class="{process_item_class}" style="color:{muted_color};">{_escape(item)}</li>'
                    for item in data.process_steps
                )
                + f"</{process_container_tag}>"
                if data.process_steps
                else ""
            )
            + "</section>"
        )

    contact_html = ""
    if data.contact_lines:
        contact_html = (
            f'<section class="mb-16 {divider_style}">'
            f'<h2 class="mb-6 text-[12px] font-bold uppercase tracking-[0.05em]" style="color:{muted_color};">Contact</h2>'
            + "".join(
                f'<p class="mb-2 text-[16px]" style="color:{muted_color};">{_escape(line)}</p>'
                for line in data.contact_lines
            )
            + "</section>"
        )

    return (
        "<!DOCTYPE html>\n\n"
        f'<html class="{html_class}" lang="en"><head>\n'
        '<meta charset="utf-8"/>\n'
        '<meta content="width=device-width, initial-scale=1.0" name="viewport"/>\n'
        f"<title>{_escape(data.title)} - NeksusJobSpec</title>\n"
        '<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;display=swap" rel="stylesheet"/>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>\n'
        '<script id="tailwind-config">tailwind.config = {darkMode: "class"};</script>\n'
        "<style>body{-webkit-font-smoothing:antialiased;}"
        f"{extra_css}"
        "</style>\n"
        "</head>\n"
        f'<body class="antialiased" style="background:{body_bg};color:{text_color};">\n'
        f'<header class="fixed left-0 top-0 z-50 flex w-full justify-center border-b px-6 backdrop-blur-sm" style="background:{body_bg};border-color:{border_color};">\n'
        f'<nav class="flex h-16 w-full items-center justify-between" style="max-width:{max_width_px}px;">\n'
        f'<span class="text-[24px] font-bold">{_escape(data.brand_name)}</span>\n'
        '<div class="flex items-center gap-6">\n'
        f'<button class="cursor-pointer rounded-lg px-6 py-2 text-[12px] font-bold uppercase tracking-[0.05em] transition-all duration-200 hover:opacity-90" style="background:{button_bg};color:{button_text};">{_escape(data.top_action_label)}</button>\n'
        "</div></nav></header>\n"
        f'<main class="mx-auto px-6 pb-16 pt-32" style="max-width:{max_width_px}px;">\n'
        f'<section style="margin-bottom:{section_gap_px}px;">\n'
        f'<h1 class="mb-4 text-[32px] font-bold leading-[1.2] tracking-[-0.01em]">{_escape(data.title)}</h1>\n'
        + (
            f'<p class="mb-6 text-[18px] leading-[1.6]" style="color:{muted_color};">{_escape(data.subtitle)}</p>\n'
            if data.subtitle
            else ""
        )
        + f'<button class="rounded-lg px-8 py-3 text-[12px] font-bold uppercase tracking-[0.05em] transition-opacity hover:opacity-90" style="background:{button_bg};color:{button_text};">'
        f"{_escape(data.apply_label)}</button>\n"
        "</section>\n"
        + (_render_classic_section("Overview", data.overview_body) if data.overview_body else "")
        + responsibilities_html
        + requirements_html
        + benefits_html
        + process_html
        + contact_html
        + "</main>\n"
        f'<footer class="border-t py-16" style="border-color:{border_color};background:{footer_bg};">'
        f'<div class="mx-auto px-6" style="max-width:{max_width_px}px;"><p class="m-0 text-[12px] font-semibold uppercase tracking-[0.05em]" style="color:{muted_color};">{_escape(footer_text)}</p></div>'
        "</footer>\n"
        "</body></html>"
    )


def _render_custom_web(spec, options: RenderOptions) -> str:
    data = _to_classic_data(spec)
    css = (options.custom_css or spec.rendering.web.css.inline).strip()
    if not css:
        raise ConfigError("Theme 'custom' requires CSS via --css or rendering.web.css.inline")

    responsibilities_html = ""
    if data.responsibilities:
        items = "".join(
            '<li class="jobspec-responsibility-item">'
            f'<h3 class="jobspec-responsibility-title">{_escape(title)}</h3>'
            f'<p class="jobspec-responsibility-body">{_escape(body)}</p>'
            "</li>"
            for _, title, body in data.responsibilities
        )
        responsibilities_html = (
            '<section class="jobspec-section jobspec-section-responsibilities">'
            '<h2 class="jobspec-section-title">Responsibilities</h2>'
            f'<ul class="jobspec-responsibility-list">{items}</ul>'
            "</section>"
        )

    requirements_html = ""
    if data.requirements:
        items = "".join(
            f'<li class="jobspec-requirement-item">{_escape(item)}</li>'
            for item in data.requirements
        )
        requirements_html = (
            '<section class="jobspec-section jobspec-section-requirements">'
            '<h2 class="jobspec-section-title">Requirements</h2>'
            f'<ul class="jobspec-requirement-list">{items}</ul>'
            "</section>"
        )

    benefits_html = ""
    if data.benefits:
        items = "".join(
            f'<li class="jobspec-benefit-item">{_escape(item)}</li>' for item in data.benefits
        )
        benefits_html = (
            '<section class="jobspec-section jobspec-section-benefits">'
            '<h2 class="jobspec-section-title">Benefits</h2>'
            f'<ul class="jobspec-benefit-list">{items}</ul>'
            "</section>"
        )

    process_html = ""
    if data.process_body or data.process_steps:
        items = "".join(
            f'<li class="jobspec-process-step">{_escape(item)}</li>' for item in data.process_steps
        )
        process_html = (
            '<section class="jobspec-section jobspec-section-process">'
            '<h2 class="jobspec-section-title">Application Process</h2>'
            + (
                f'<p class="jobspec-process-body">{_escape(data.process_body)}</p>'
                if data.process_body
                else ""
            )
            + (f'<ol class="jobspec-process-steps">{items}</ol>' if items else "")
            + "</section>"
        )

    contact_html = ""
    if data.contact_lines:
        lines = "".join(
            f'<p class="jobspec-contact-line">{_escape(line)}</p>' for line in data.contact_lines
        )
        contact_html = (
            '<section class="jobspec-section jobspec-section-contact">'
            '<h2 class="jobspec-section-title">Contact</h2>'
            f"{lines}</section>"
        )

    return (
        "<!DOCTYPE html>\n\n"
        '<html lang="en"><head>\n'
        '<meta charset="utf-8"/>\n'
        '<meta content="width=device-width, initial-scale=1.0" name="viewport"/>\n'
        f"<title>{_escape(data.title)} - NeksusJobSpec</title>\n"
        "<style>\n"
        f"{css}\n"
        "</style>\n"
        "</head>\n"
        '<body class="jobspec-page">\n'
        '<header class="jobspec-header">\n'
        '<div class="jobspec-header-inner">\n'
        f'<div class="jobspec-brand">{_escape(data.brand_name)}</div>\n'
        f'<div class="jobspec-header-action">{_escape(data.top_action_label)}</div>\n'
        "</div>\n"
        "</header>\n"
        '<main class="jobspec-main">\n'
        '<section class="jobspec-section jobspec-section-hero">\n'
        f'<h1 class="jobspec-title">{_escape(data.title)}</h1>\n'
        f'<p class="jobspec-subtitle">{_escape(data.subtitle)}</p>\n'
        f'<div class="jobspec-apply">{_escape(data.apply_label)}</div>\n'
        "</section>\n"
        + (
            '<section class="jobspec-section jobspec-section-overview">'
            '<h2 class="jobspec-section-title">Overview</h2>'
            f'<p class="jobspec-overview">{_escape(data.overview_body)}</p>'
            "</section>"
            if data.overview_body
            else ""
        )
        + responsibilities_html
        + requirements_html
        + benefits_html
        + process_html
        + contact_html
        + "</main>\n"
        '<footer class="jobspec-footer">\n'
        f'<div class="jobspec-footer-inner">{_escape(data.footer_text)}</div>\n'
        "</footer>\n"
        "</body></html>"
    )


def _build_soft_professional_context(spec) -> dict[str, object]:
    data = _to_soft_professional_data(spec)
    return {
        "tailwind_config": TAILWIND_CONFIG,
        "base_style": BASE_STYLE,
        "title": data.title,
        "location": data.location,
        "salary": data.salary,
        "employment": data.employment,
        "apply_label": data.apply_label,
        "campaign_notice": data.campaign_notice,
        "about_title": data.about_title,
        "about_body": data.about_body,
        "responsibilities_title": data.responsibilities_title,
        "responsibility_cards": data.responsibility_cards[:3],
        "requirements_title": data.requirements_title,
        "requirements": data.requirements,
        "quick_facts": data.quick_facts,
        "benefits_title": data.benefits_title,
        "benefits": data.benefits,
        "map_image": data.map_image,
        "map_alt": data.map_alt,
        "map_label": data.map_label,
        "cta_title": data.cta_title,
        "cta_body": data.cta_body,
        "cta_label": data.cta_label,
        "footer_brand": data.footer_brand,
        "footer_icons": data.footer_icons,
    }


def _build_classic_context(spec, *, dark: bool) -> dict[str, object]:
    data = _to_classic_data(spec)
    classic_config = spec.rendering.web.classic
    palette = classic_config.palette
    footer_text = (
        data.footer_text
        if classic_config.footer_style == "minimal"
        else f"{data.brand_name} · {data.title}"
    )
    return {
        "html_class": "dark" if dark else "light",
        "title": data.title,
        "brand_name": data.brand_name,
        "top_action_label": data.top_action_label,
        "subtitle": data.subtitle,
        "apply_label": data.apply_label,
        "overview_body": data.overview_body,
        "responsibilities": data.responsibilities,
        "requirements": data.requirements,
        "benefits": data.benefits,
        "process_body": data.process_body,
        "process_steps": data.process_steps,
        "contact_lines": data.contact_lines,
        "footer_text": footer_text,
        "body_bg": palette.background or ("#141313" if dark else "#f8f9fb"),
        "text_color": palette.text or ("#e5e2e1" if dark else "#191c1e"),
        "muted_color": palette.muted_text or ("#c4c7c8" if dark else "#444748"),
        "border_color": palette.border or ("#444748" if dark else "#c4c7c7"),
        "card_bg": palette.card_background or ("#1c1b1b" if dark else "#f2f4f6"),
        "footer_bg": palette.footer_background or ("#0e0e0e" if dark else "#ffffff"),
        "button_bg": palette.button_background or "#000000",
        "button_text": palette.button_text or "#ffffff",
        "max_width_px": classic_config.content_max_width_px,
        "section_gap_px": classic_config.section_gap_px,
        "responsibilities_style": classic_config.responsibilities_style,
        "requirements_icon": "check" if classic_config.requirements_marker == "check" else "remove",
        "process_style": classic_config.process_style,
    }


def _build_custom_context(spec) -> dict[str, object]:
    data = _to_classic_data(spec)
    normalized = normalize_jobspec_for_render(spec)
    return {
        "title": data.title,
        "brand_name": data.brand_name,
        "top_action_label": data.top_action_label,
        "subtitle": data.subtitle,
        "apply_label": data.apply_label,
        "overview_body": data.overview_body,
        "responsibilities": data.responsibilities,
        "requirements": data.requirements,
        "benefits": data.benefits,
        "process_body": data.process_body,
        "process_steps": data.process_steps,
        "contact_lines": data.contact_lines,
        "footer_text": data.footer_text,
        "spec": spec.model_dump(mode="json"),
        "components": [component.model_dump(mode="json") for component in normalized.components],
    }


def _render_with_theme_package(spec, options: RenderOptions) -> str:
    package = resolve_theme_package(options.theme, spec.rendering.web.template)
    if package.theme_id == "soft-professional":
        context = _build_soft_professional_context(spec)
    elif package.theme_id == "classic":
        context = _build_classic_context(spec, dark=False)
    elif package.theme_id == "classic-dark":
        context = _build_classic_context(spec, dark=True)
    else:
        context = _build_custom_context(spec)
    return render_theme(package, context=context, custom_css=options.custom_css)


def render_html(spec, options: RenderOptions) -> str:
    """Render a JobSpec into HTML."""
    return _render_with_theme_package(spec, options)
