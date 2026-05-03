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
        supported_formats=["markdown", "html", "json"],
        css_embedded=True,
        layout_notes="Classic card layout and serif typography in HTML.",
        token_hints=["density:medium", "tone:neutral", "contrast:balanced"],
    ),
    "compact": ThemeMetadata(
        name="compact",
        description="Denser layout optimized for quick scanning.",
        supported_formats=["markdown", "html", "json"],
        css_embedded=True,
        layout_notes="Reduced spacing and tighter line heights.",
        token_hints=["density:high", "tone:pragmatic", "contrast:high"],
    ),
    "modern": ThemeMetadata(
        name="modern",
        description="Contemporary sans-serif layout with softer surfaces.",
        supported_formats=["markdown", "html", "json"],
        css_embedded=True,
        layout_notes="Rounded container, airy spacing, and system sans stack.",
        token_hints=["density:medium", "tone:modern", "contrast:soft"],
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
:root { color-scheme: light; }
body {
  margin: 0;
  background: linear-gradient(180deg, #f4f7fb 0%, #eef2f8 100%);
  color: #0f172a;
  font-family: 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  line-height: 1.6;
}
main {
  max-width: 860px;
  margin: 2rem auto;
  background: #ffffff;
  border: 1px solid #dbe4f0;
  border-radius: 14px;
  padding: 1.7rem;
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.07);
}
h1, h2 { line-height: 1.25; color: #0b2545; }
h1 { margin-top: 0; }
section + section { margin-top: 1.3rem; }
ul { padding-left: 1.25rem; }
li + li { margin-top: 0.35rem; }
""".strip(),
}


def list_theme_names() -> list[str]:
    """Return stable ordered theme names."""
    return ["default", "compact", "modern"]


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
