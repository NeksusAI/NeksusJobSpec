"""HTML renderer."""

from __future__ import annotations

import html
from dataclasses import dataclass

from neksus.core.jobspec.models import (
    BenefitsComponent,
    FeatureGridComponent,
    HeroBannerComponent,
    HeroComponent,
    ListComponent,
    LocationMapComponent,
    MetaChipsComponent,
    MetaPanelComponent,
    RichTextComponent,
)
from neksus.core.jobspec.rendering.normalize import normalize_jobspec_for_render
from neksus.core.jobspec.rendering.options import RenderOptions

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
class StitchData:
    title: str
    location: str
    data_location: str
    salary: str
    employment: str
    apply_label: str
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


def _escape(value: str) -> str:
    return html.escape(value, quote=True)


def _component_by_type(components, kind: str):
    for item in components:
        if item.type == kind:
            return item
    return None


def _to_stitch_data(spec) -> StitchData:
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

    title = hero.title if isinstance(hero, HeroComponent) and hero.title else normalized.title
    apply_label = normalized.apply_label or "Apply Now"

    location = "San Francisco, CA"
    salary = "$180k – $240k"
    employment = "Full-time"
    if isinstance(chips, MetaChipsComponent):
        for item in chips.items:
            label = item.label.lower()
            if "location" in label:
                location = item.value
            elif "salary" in label or "comp" in label:
                salary = item.value
            elif "type" in label or "employment" in label:
                employment = item.value

    about_title = "About the Role"
    about_body = ""
    if isinstance(about, RichTextComponent):
        about_title = about.title or about_title
        about_body = about.body

    responsibilities_title = "Key Responsibilities"
    responsibility_cards: list[tuple[str, str, str]] = []
    if isinstance(grid, FeatureGridComponent):
        responsibilities_title = grid.title or responsibilities_title
        for item in grid.items:
            responsibility_cards.append((item.icon or "architecture", item.title, item.body))

    requirements_title = "Requirements"
    requirements: list[str] = []
    if isinstance(req, ListComponent):
        requirements_title = req.title or requirements_title
        requirements = list(req.items)

    quick_facts = [
        ("Industry", "FinTech / CLI Tech"),
        ("Team Size", "12 Engineers"),
        ("Remote Policy", "Hybrid (3 Days)"),
        ("Reports to", "CTO"),
    ]
    if isinstance(meta, MetaPanelComponent) and len(meta.facts) >= 4:
        quick_facts = [(item.label, item.value) for item in meta.facts[:4]]

    benefits_title = "Our Benefits"
    benefits_tags = ["Unlimited PTO", "Equity Options", "Health/Dental", "Tech Stipend"]
    if isinstance(benefits, BenefitsComponent):
        benefits_title = benefits.title or benefits_title
        tags: list[str] = []
        for item in benefits.items:
            if isinstance(item, str):
                tags.append(item)
            else:
                tags.append(item.get("text", ""))
        benefits_tags = [item for item in tags if item] or benefits_tags

    map_image = "https://lh3.googleusercontent.com/aida-public/AB6AXuBP7eiY08JzrrHzVBNG0b8cSa2T8AYepZGIzOqEG3IThlXtGYg7jZ1GKMw8NfMQB5eYFiZtXfAaKealTDv44YaN5uDMWIIamTqBS2mnvSyQYp4wd86_d0EKUbsonXAanZ-B7BGX5A3R85JBXMRTXMtujqjO3LeXDN7z4Zot5YRLbpJZf5_Ln9x7mP2y-IDGT11jB7xbIiBvu1D4o3lj1-hwtbjWAn1_E6ZmrS8aWWDhyBK1EMBIWqa-EBAumbiO43oBtKZaEUk0MNcI"
    map_alt = "Map"
    if isinstance(banner, HeroBannerComponent):
        map_image = banner.image_url
        if banner.alt:
            map_alt = banner.alt

    map_label = "Main HQ: 450 Mission St, San Francisco"
    if isinstance(location_map, LocationMapComponent) and location_map.address:
        map_label = f"Main HQ: {location_map.address}"
    cta_title = "Have Questions?"
    cta_body = (
        "Reach out to our engineering recruitment team to learn more about the technical stack."
    )
    cta_label = "Contact Recruiting"

    return StitchData(
        title=title,
        location=location,
        data_location=location.split(",")[0].strip() if "," in location else location,
        salary=salary,
        employment=employment,
        apply_label=apply_label,
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
    )


def _render_stitch_web(spec, options: RenderOptions) -> str:
    data = _to_stitch_data(spec)

    cards = data.responsibility_cards or [
        (
            "architecture",
            "System Design",
            "Design end-to-end microservices architectures optimized for low-latency terminal interactions.",
        ),
        (
            "cloud_sync",
            "Cloud Orchestration",
            "Manage complex Kubernetes clusters and automated CI/CD pipelines for CLI binary distributions.",
        ),
        (
            "security",
            "Security & Reliability",
            "Implement zero-trust security models and 99.99% uptime strategies across our entire CLI-to-Cloud infrastructure.",
        ),
    ]
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
        f'<button class="bg-primary text-on-primary px-6 py-3 font-semibold rounded hover:bg-primary-container transition-colors">{_escape(data.apply_label)}</button>\n'
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
        '<span class="text-xs font-label-sm uppercase tracking-widest">JobTerminal CLI / v2.4.0-stable</span>\n'
        '<div class="flex gap-md">\n'
        '<span class="material-symbols-outlined text-sm" data-icon="share">share</span>\n'
        '<span class="material-symbols-outlined text-sm" data-icon="report">report</span>\n'
        "</div>\n"
        "</footer>\n"
        "</div>\n"
        "</body></html>"
    )


def render_html(spec, options: RenderOptions) -> str:
    """Render a JobSpec into HTML."""
    return _render_stitch_web(spec, options)
