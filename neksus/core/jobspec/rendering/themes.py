"""Built-in rendering themes and metadata."""

from __future__ import annotations

from pydantic import BaseModel

from neksus.core.errors import ConfigError


class ThemeMetadata(BaseModel):
    """Theme metadata surfaced by CLI commands."""

    name: str
    description: str
    supported_formats: list[str]
    css_embedded: bool
    layout_notes: str
    token_hints: list[str]


_THEME_METADATA: dict[str, ThemeMetadata] = {
    "soft-professional": ThemeMetadata(
        name="soft-professional",
        description="Modern editorial job-detail layout inspired by professional career sites.",
        supported_formats=["web"],
        css_embedded=True,
        layout_notes="Header + hero + two-column content/sidebar + branded footer layout.",
        token_hints=["density:medium", "tone:professional", "contrast:balanced"],
    )
}


_THEME_CSS: dict[str, str] = {
    "soft-professional": """
:root {
  color-scheme: light;
  --sp-bg: #e7eaef;
  --sp-surface: #ffffff;
  --sp-text: #1f2e3d;
  --sp-muted: #5f6d7f;
  --sp-line: #d3dae4;
  --sp-primary: #ef9f2f;
  --sp-primary-strong: #d2861f;
  --sp-ink: #0f2733;
  --sp-soft: #eef4fa;
  --sp-brand: #0f786f;
  --sp-brand-dark: #0a4d49;
  --sp-radius: 14px;
  --sp-shadow: 0 22px 42px -36px rgba(12, 20, 31, 0.4);
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: "Inter", "Segoe UI", Arial, sans-serif;
  background: var(--sp-bg);
  color: var(--sp-text);
  line-height: 1.58;
}
.material-symbols-rounded {
  font-variation-settings: "FILL" 1, "wght" 500, "GRAD" 0, "opsz" 20;
  vertical-align: -0.24em;
}
.jobspec-page {
  width: min(1090px, 100% - 36px);
  margin: 0 auto 26px;
  background: var(--sp-surface);
  border: 1px solid #cfd7e1;
  border-top: 0;
  border-radius: 0;
  box-shadow: var(--sp-shadow);
  overflow: hidden;
}
.jobspec-region { margin: 0; }
.jobspec-region--header {
  background: #fff;
  border-bottom: 1px solid #cfd7e1;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  grid-template-areas:
    "brand actions"
    "nav nav";
  padding: 0 28px;
}
.jobspec-region--hero {
  background: #f5f8fa;
  border-bottom: 1px solid #d7dee5;
}
.jobspec-region--footer {
  background: var(--sp-brand-dark);
  margin-top: 0;
}
.jobspec-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 26px;
  padding: 22px 26px 30px;
}
.jobspec-main .component { border: 0; background: transparent; padding: 16px 0; margin: 0; box-shadow: none; }
.jobspec-main .component + .component { border-top: 0; }
.jobspec-sidebar .component {
  border: 1px solid var(--sp-line);
  border-radius: var(--sp-radius);
  background: #fff;
  padding: 16px 16px 14px;
  margin-bottom: 12px;
  box-shadow: 0 4px 12px rgba(15, 23, 36, 0.04);
}
.component h2 { margin: 0 0 10px; font-size: clamp(1.2rem, 1.4vw, 1.52rem); line-height: 1.24; color: var(--sp-ink); letter-spacing: -0.014em; }
.component h3 { margin: 0 0 8px; font-size: 1rem; color: var(--sp-ink); letter-spacing: -0.008em; }
.component p { margin: 0 0 11px; color: var(--sp-text); font-size: 0.97rem; }
.component ul, .component ol { margin: 0; padding-left: 1.15rem; }
.component li + li { margin-top: 6px; }
.jobspec-main .component--rich_text p,
.jobspec-main .component--company_profile p,
.jobspec-main .component--legal p {
  max-width: 76ch;
}

.brand-header {
  border: 0;
  border-radius: 0;
  padding: 18px 0 10px;
  background: transparent;
  grid-area: brand;
}
.brand-header .brand-row { display: flex; align-items: center; gap: 12px; }
.brand-header .brand-name,
.brand-header .brand-name-link {
  font-size: clamp(1.7rem, 2.15vw, 2.05rem);
  letter-spacing: -0.026em;
  color: var(--sp-brand);
  text-decoration: none;
  font-weight: 900;
}

.component--nav_links,
.component--header_actions {
  border: 0;
  border-radius: 0;
  background: transparent;
  padding: 0;
  margin: 0;
}
.component--nav_links { grid-area: nav; padding: 0 0 12px; }
.component--header_actions { grid-area: actions; display: flex; align-items: center; }
.component--nav_links ul,
.component--social_links ul,
.component--footer_brand ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.component--nav_links li { display: inline-block; margin-right: 18px; }
.component--nav_links a { color: var(--sp-muted); text-decoration: none; font-weight: 600; font-size: 0.9rem; }
.component--nav_links a:hover { color: var(--sp-primary); }
.component--nav_links a.is-active {
  color: var(--sp-brand-dark);
  border-bottom: 2px solid var(--sp-brand);
  padding-bottom: 7px;
}
.component--header_actions .header-actions { display: flex; justify-content: flex-end; gap: 10px; }

.hero-banner-image,
.hero-banner-image figure {
  margin: 0;
  border: 0;
  border-radius: 0;
  overflow: hidden;
  padding: 0;
}
.hero-banner-image img {
  width: 100%;
  display: block;
  max-height: 520px;
  object-fit: cover;
}
.hero-banner {
  border: 0;
  border-radius: 0;
  background: transparent;
  padding: 30px 28px 12px;
}
.hero-banner h2 {
  font-size: clamp(2.32rem, 3.4vw, 3.22rem);
  margin-bottom: 10px;
  color: #0e6a63;
}
.hero-banner p:first-of-type {
  font-size: 1.08rem;
  color: #324353;
}

.component--meta_chips {
  border: 0;
  border-radius: 0;
  background: transparent;
  padding: 0 28px 24px;
  margin: 0;
}
.component--meta_chips ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.component--meta_chips li {
  background: var(--sp-soft);
  border: 1px solid #d3dce8;
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 0.83rem;
  color: #40566f;
}
.chip-icon { font-size: 15px; margin-right: 4px; color: var(--sp-brand); }

.cta-link,
.header-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  border-radius: 999px;
  padding: 10px 20px;
  font-weight: 800;
  text-decoration: none;
  border: 1px solid transparent;
}
.header-action--sm { min-height: 36px; padding: 7px 13px; font-size: 0.87rem; }
.header-action--md { min-height: 42px; padding: 9px 18px; font-size: 0.92rem; }
.header-action--lg { min-height: 48px; padding: 11px 22px; font-size: 0.97rem; }
.cta-link,
.header-action--primary,
.header-action--intent-primary {
  background: var(--sp-primary);
  color: #17202a;
}
.cta-link:hover,
.header-action--primary:hover,
.header-action--intent-primary:hover { background: var(--sp-primary-strong); }
.header-action--secondary,
.header-action--intent-secondary {
  background: #fff;
  color: var(--sp-primary-strong);
  border-color: #bfd0f8;
}

.component--feature_grid .feature-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}
.feature-card {
  border: 1px solid #d4dbe4;
  border-radius: 12px;
  padding: 14px 14px;
  background: #fdfefe;
}
.feature-card__icon {
  display: inline-block;
  margin-bottom: 8px;
  color: var(--sp-primary-strong);
  font-size: 18px;
}

.component--meta_panel ul { list-style: none; padding: 0; margin: 0 0 12px; }
.component--meta_panel li { padding: 7px 0; border-bottom: 1px solid #e6ebf1; }
.component--meta_panel li:last-child { border-bottom: 0; }
.fact-icon { color: var(--sp-brand); margin-right: 6px; font-size: 16px; }
.component--meta_panel p { margin-bottom: 8px; }
.component--meta_panel p:last-child { margin-bottom: 0; }

.component--benefits {
  background: #0e6a63;
  border-color: #0a5a54;
  border-radius: 12px;
  padding: 16px 16px 14px;
}
.component--benefits h2,
.component--benefits p,
.component--benefits li { color: #effaf8; }
.component--benefits ul {
  list-style: none;
  padding-left: 0;
}
.component--benefits li {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  line-height: 1.5;
}

.benefits-icon,
.social-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  margin-top: 1px;
  font-size: 16px;
  color: #bde4df;
}
.component--social_links li + li { margin-top: 8px; }
.component--social_links a {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--sp-text);
  text-decoration: none;
}
.component--social_links a:hover { color: var(--sp-primary); }
.component--location_map .map-frame-wrap {
  border: 1px solid #d9dfe7;
  border-radius: 8px;
  overflow: hidden;
  margin: 10px 0;
  background: #eef3fb;
}
.component--location_map .map-frame {
  display: block;
  width: 100%;
  border: 0;
}
.component--location_map p { margin-bottom: 8px; }

.component--footer_brand {
  border: 0;
  border-radius: 0;
  background: transparent;
  padding: 26px 28px;
}
.component--footer_brand h2,
.component--footer_brand h3,
.component--footer_brand p,
.component--footer_brand a { color: #dce8e6; }
.component--footer_brand h3 {
  color: #ffffff;
  font-size: 2rem;
  letter-spacing: -0.02em;
}
.component--footer_brand p {
  color: #d4e3df;
  max-width: 90ch;
}

.share-links,
.print-link {
  margin: 0 28px 8px;
}
.share-links,
.print-link {
  display: inline-block;
  margin-top: 10px;
}
.share-trigger,
.print-trigger {
  background: transparent;
  border: 0;
  color: var(--sp-muted);
  cursor: pointer;
  font: inherit;
  padding: 0;
}
.share-trigger:hover,
.print-trigger:hover { color: var(--sp-primary); }

@media (min-width: 860px) {
  .component--feature_grid .feature-grid { grid-template-columns: 1fr 1fr; }
}
@media (min-width: 980px) {
  .jobspec-layout {
    grid-template-columns: minmax(0, 1fr) 310px;
    align-items: start;
    column-gap: 22px;
  }
  .jobspec-sidebar {
    position: sticky;
    top: 10px;
    padding-bottom: 8px;
  }
}
@media (max-width: 979px) {
  .jobspec-region--header {
    grid-template-columns: 1fr;
    grid-template-areas:
      "brand"
      "actions"
      "nav";
    padding: 0 16px;
  }
  .hero-banner,
  .component--meta_chips,
  .share-links,
  .print-link,
  .component--footer_brand { padding-left: 16px; padding-right: 16px; }
  .jobspec-layout { padding: 16px 16px 22px; }
}
""".strip()
}


def list_theme_names() -> list[str]:
    """Return stable ordered theme names."""
    return ["soft-professional"]


def get_theme_metadata(name: str) -> ThemeMetadata:
    """Return metadata for a known built-in theme."""
    if name not in _THEME_METADATA:
        raise ConfigError(f"Unknown theme: {name}")
    return _THEME_METADATA[name]


def list_theme_metadata() -> list[ThemeMetadata]:
    """Return metadata for all built-in themes."""
    return [get_theme_metadata(name) for name in list_theme_names()]


def get_theme_css(name: str) -> str:
    """Return built-in CSS for a known theme."""
    if name not in _THEME_CSS:
        raise ConfigError(f"Unknown theme: {name}")
    return _THEME_CSS[name]
