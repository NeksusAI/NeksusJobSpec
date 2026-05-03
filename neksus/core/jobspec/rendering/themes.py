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
    "default": ThemeMetadata(
        name="default",
        description="Balanced editorial layout with readable spacing.",
        supported_formats=["web"],
        css_embedded=True,
        layout_notes="Classic card layout and serif typography in HTML.",
        token_hints=["density:medium", "tone:neutral", "contrast:balanced"],
    ),
    "compact": ThemeMetadata(
        name="compact",
        description="Denser layout optimized for quick scanning.",
        supported_formats=["web"],
        css_embedded=True,
        layout_notes="Reduced spacing and tighter line heights.",
        token_hints=["density:high", "tone:pragmatic", "contrast:high"],
    ),
    "modern": ThemeMetadata(
        name="modern",
        description="Contemporary sans-serif layout with softer surfaces.",
        supported_formats=["web"],
        css_embedded=True,
        layout_notes="Rounded container, airy spacing, and system sans stack.",
        token_hints=["density:medium", "tone:modern", "contrast:soft"],
    ),
    "classic": ThemeMetadata(
        name="classic",
        description="Nordic vacancy-page layout with branded hero and sidebar facts.",
        supported_formats=["web"],
        css_embedded=True,
        layout_notes="Two-column desktop layout with strong masthead and dark footer brand block.",
        token_hints=["density:medium", "tone:editorial", "contrast:strong"],
    ),
}


_THEME_CSS: dict[str, str] = {
    "default": """
:root { color-scheme: light; }
body {
  margin: 0;
  background: #f7f8fa;
  color: #1f2937;
  font-family: Georgia, 'Times New Roman', serif;
  line-height: 1.55;
}
main {
  max-width: 860px;
  margin: 2rem auto;
  background: #ffffff;
  border: 1px solid #d9dce3;
  border-radius: 10px;
  padding: 1.5rem;
}
h1, h2 { line-height: 1.25; }
h1 { margin-top: 0; }
section + section { margin-top: 1.25rem; }
ul { padding-left: 1.25rem; }
li + li { margin-top: 0.35rem; }
""".strip(),
    "compact": """
:root { color-scheme: light; }
body {
  margin: 0;
  background: #ffffff;
  color: #111827;
  font-family: Arial, Helvetica, sans-serif;
  line-height: 1.4;
}
main {
  max-width: 920px;
  margin: 1rem auto;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 1rem;
}
h1, h2 { line-height: 1.2; margin-bottom: 0.4rem; }
h1 { margin-top: 0; }
section + section { margin-top: 0.8rem; }
ul { padding-left: 1.1rem; margin: 0.4rem 0 0; }
li + li { margin-top: 0.2rem; }
""".strip(),
    "modern": """
:root {
  color-scheme: light;
  --brand-teal: #0b7a77;
  --brand-teal-dark: #04504f;
  --brand-orange: #f6a033;
  --surface: #f3f4f6;
  --page-bg: #e8eaec;
  --text: #22303d;
  --muted: #5d6a75;
  --line: #d5d8dd;
  --sidebar: #deece8;
}
* { box-sizing: border-box; }
html, body {
  margin: 0;
  padding: 0;
}
body {
  background: linear-gradient(180deg, #f0f2f4 0%, #e6e8eb 100%);
  color: var(--text);
  font-family: "Nunito Sans", "Segoe UI", Arial, sans-serif;
  line-height: 1.55;
}
.jobspec-page {
  width: min(1120px, 100% - 24px);
  margin: 18px auto 36px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 8px;
  overflow: hidden;
}
.jobspec-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
}
.jobspec-main .component {
  padding: 0 30px 20px;
}
.jobspec-sidebar {
  padding: 0 14px 20px;
}
.jobspec-sidebar .component {
  margin: 0 0 14px;
  padding: 14px 16px 16px;
  background: var(--sidebar);
  border: 1px solid #c9ddd7;
}
.jobspec-fullwidth .component {
  padding: 0;
  margin: 0;
}
.component h2 {
  margin: 0 0 10px;
  color: #1f3040;
  font-size: clamp(1.3rem, 1.7vw, 1.95rem);
  line-height: 1.2;
}
.component p, .component li, .component blockquote {
  font-size: 1.02rem;
}
.brand-header {
  background: #efefef;
  border-bottom: 1px solid #c6c8cc;
  padding: 14px 28px;
}
.brand-header .brand-name,
.brand-header .brand-name-link {
  font-weight: 800;
  color: var(--brand-teal);
  text-decoration: none;
  letter-spacing: -0.02em;
  font-size: clamp(2.1rem, 4vw, 3rem);
}
.hero-banner-image {
  border-top: 1px solid #a5b3b2;
  border-bottom: 1px solid #bcc8c7;
}
.hero-banner-image figure { margin: 0; }
.hero-banner-image img {
  width: 100%;
  display: block;
}
.hero-banner {
  padding-top: 18px;
}
.hero-banner h2 {
  color: var(--brand-teal);
  font-size: clamp(2rem, 3vw, 3rem);
}
.hero-banner p {
  margin: 0 0 10px;
}
.cta-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  padding: 10px 22px;
  min-width: 220px;
  font-weight: 700;
  text-decoration: none;
  background: var(--brand-orange);
  color: #111;
}
.quote-feature blockquote {
  margin: 0;
  font-style: italic;
  border-left: 4px solid #a7b8c7;
  padding-left: 12px;
}
.quote-feature cite {
  display: block;
  margin-top: 8px;
  color: var(--muted);
}
.meta-panel ul,
.social-panel ul,
.footer-brand ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.meta-panel li {
  padding: 6px 0;
}
.social-panel li {
  display: inline-block;
  margin-right: 10px;
  margin-bottom: 8px;
}
.share-links,
.print-link {
  margin: 6px 30px;
}
.share-trigger,
.print-trigger {
  background: transparent;
  border: 0;
  padding: 0;
  cursor: pointer;
  color: #2f617f;
  font: inherit;
}
.footer-brand {
  background: var(--brand-teal-dark);
  padding: 24px 30px 30px;
}
.footer-brand h2, .footer-brand h3, .footer-brand p, .footer-brand a {
  color: #e8f5f4;
}
@media (min-width: 980px) {
  .jobspec-layout {
    grid-template-columns: minmax(0, 1fr) 300px;
    column-gap: 10px;
    align-items: start;
  }
  .jobspec-sidebar {
    position: sticky;
    top: 16px;
    max-height: calc(100vh - 24px);
    overflow: auto;
    padding-top: 8px;
  }
}
""".strip(),
    "classic": """
:root {
  color-scheme: light;
  --teal: #0b7a77;
  --teal-dark: #04504f;
  --bg: #e3e3e3;
  --surface: #f2f2f2;
  --text: #2a2f36;
  --muted: #5c6672;
  --sidebar: #dcebe8;
  --accent: #f6a033;
  --line: #d2d2d2;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: "Nunito Sans", "Segoe UI", Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.55;
}
.jobspec-page {
  width: min(1120px, 100% - 28px);
  margin: 0 auto 36px;
  background: var(--surface);
  border: 1px solid var(--line);
}
.jobspec-page > h1 {
  margin: 0;
  padding: 26px 28px 10px;
  color: var(--teal);
  font-size: clamp(2rem, 3.2vw, 2.9rem);
  letter-spacing: -0.015em;
}
.jobspec-page > p { margin: 0; padding: 8px 28px 18px; }
.jobspec-fullwidth .component { padding: 0; margin: 0; }
.jobspec-layout { display: grid; grid-template-columns: minmax(0, 1fr); gap: 0; }
.jobspec-main .component { padding: 0 28px 18px; }
.jobspec-sidebar .component {
  margin: 0 16px 16px 0;
  padding: 14px 16px 18px;
  background: var(--sidebar);
}
.component h2 {
  margin: 0 0 10px;
  color: #1e2d3d;
  font-size: 1.95rem;
}
.component p, .component li, .component blockquote, .component cite {
  color: #24323d;
  font-size: 1.02rem;
}
.brand-header {
  background: #efefef;
  border-bottom: 1px solid #c8c8c8;
  padding: 16px 28px;
}
.brand-header .brand-row { display: flex; align-items: center; }
.brand-header .brand-name, .brand-header .brand-name-link {
  color: var(--teal);
  font-size: 3rem;
  font-weight: 700;
  text-decoration: none;
  letter-spacing: -0.03em;
}
.hero-banner-image { border-top: 1px solid #95a5a5; border-bottom: 1px solid #b1c0bf; }
.hero-banner-image figure { margin: 0; }
.hero-banner-image img { width: 100%; display: block; }
.hero-banner { padding-top: 14px; }
.hero-banner p { margin: 0; }
.hero-banner .cta-link, .apply-strip .cta-link, .repeat-cta .cta-link, .jobspec-page > p .cta-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--accent);
  color: #111;
  border-radius: 999px;
  min-width: 245px;
  padding: 10px 22px;
  font-size: 1rem;
  font-weight: 700;
  text-decoration: none;
}
.section-list ol, .section-list ul, .process-box ol { margin: 8px 0 0; padding-left: 1.5rem; }
.quote-feature blockquote {
  margin: 0;
  font-style: italic;
  border-left: 3px solid #a7b8c7;
  padding-left: 10px;
}
.quote-feature cite { margin-top: 8px; display: block; color: var(--muted); }
.benefits-grid ul { list-style: none; padding-left: 0; margin: 0; }
.benefits-grid li::before { content: "• "; color: #39566f; }
.meta-panel ul, .social-panel ul { list-style: none; margin: 0; padding: 0; }
.meta-panel li { padding: 6px 0; }
.social-panel li { display: inline-block; margin: 0 10px 8px 0; }
.social-panel a, .map-panel a, .share-links a, .print-link a, .share-trigger, .print-trigger {
  color: #2f617f;
  text-decoration: none;
  font: inherit;
  background: transparent;
  border: 0;
  padding: 0;
  cursor: pointer;
}
.social-panel a:hover, .map-panel a:hover, .share-links a:hover, .print-link a:hover, .share-trigger:hover, .print-trigger:hover { text-decoration: underline; }
.footer-brand { background: #024b4a; padding: 22px 28px 26px; }
.footer-brand h2, .footer-brand h3, .footer-brand p, .footer-brand a { color: #e8f5f4; }
.footer-brand ul { list-style: none; padding: 0; margin: 8px 0 0; }
.share-links, .print-link { margin: 0 28px 8px; color: var(--muted); font-size: 0.95rem; }
@media (min-width: 980px) {
  .jobspec-layout {
    grid-template-columns: minmax(0, 1fr) 290px;
    column-gap: 10px;
    align-items: start;
  }
  .jobspec-sidebar {
    position: sticky;
    top: 12px;
    align-self: start;
    max-height: calc(100vh - 24px);
    overflow: auto;
    padding-top: 8px;
  }
}
""".strip(),
}


def list_theme_names() -> list[str]:
    """Return stable ordered theme names."""
    return ["default", "compact", "modern", "classic"]


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
