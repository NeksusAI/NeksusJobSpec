"""Built-in rendering themes and metadata."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from neksus_jobspec.errors import ConfigError, FileSystemError


class ThemeMetadata(BaseModel):
    """Theme metadata surfaced by CLI commands."""

    name: str
    description: str
    supported_formats: list[str]
    css_embedded: bool
    layout_notes: str
    token_hints: list[str]


_THEME_METADATA: dict[str, ThemeMetadata] = {
    "custom": ThemeMetadata(
        name="custom",
        description="User-supplied CSS defines the full visual theme.",
        supported_formats=["web"],
        css_embedded=False,
        layout_notes="Semantic HTML contract rendered without built-in theme styles.",
        token_hints=["density:user-defined", "tone:user-defined", "contrast:user-defined"],
    ),
    "classic": ThemeMetadata(
        name="classic",
        description="Minimalist light job posting layout aligned with classic prototype.",
        supported_formats=["web"],
        css_embedded=True,
        layout_notes="Fixed top bar, single-column editorial sections, understated footer.",
        token_hints=["density:medium", "tone:minimal", "contrast:high"],
    ),
    "classic-dark": ThemeMetadata(
        name="classic-dark",
        description="Minimalist dark job posting layout aligned with dark prototype.",
        supported_formats=["web"],
        css_embedded=True,
        layout_notes="Dark top bar and body palette with same classic section structure.",
        token_hints=["density:medium", "tone:minimal-dark", "contrast:high"],
    ),
    "soft-professional": ThemeMetadata(
        name="soft-professional",
        description="Modern editorial job-detail layout inspired by professional career sites.",
        supported_formats=["web"],
        css_embedded=True,
        layout_notes="Header + hero + two-column content/sidebar + branded footer layout.",
        token_hints=["density:medium", "tone:professional", "contrast:balanced"],
    ),
}

_THEME_CSS_DIR = Path(__file__).with_name("theme_css")


def _read_css_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise FileSystemError(f"Failed to read CSS template: {path}") from exc


def list_theme_names() -> list[str]:
    """List available built-in theme names."""
    return sorted(_THEME_METADATA)


def list_theme_metadata() -> list[ThemeMetadata]:
    """List built-in theme metadata sorted by name."""
    return [_THEME_METADATA[name] for name in sorted(_THEME_METADATA)]


def get_theme_metadata(name: str) -> ThemeMetadata:
    """Return metadata for a specific built-in theme."""
    if name in _THEME_METADATA:
        return _THEME_METADATA[name]
    allowed = ", ".join(sorted(_THEME_METADATA))
    raise ConfigError(f"Unknown theme: {name}. Available themes: {allowed}")


def get_theme_css(theme_or_template: str) -> str:
    """Return CSS for a built-in theme name or a user CSS template path."""
    key = theme_or_template.strip()
    if not key:
        raise ConfigError("Theme/template value must not be empty")

    if key in _THEME_METADATA:
        if key == "custom":
            raise ConfigError(
                "Theme 'custom' is package-based and has no single built-in CSS file. "
                "Provide a custom theme directory with manifest/template/css assets."
            )
        return _read_css_file(_THEME_CSS_DIR / f"{key}.css")

    template_path = Path(key)
    if template_path.suffix.lower() == ".css" and template_path.exists():
        return _read_css_file(template_path)

    allowed = ", ".join(sorted(_THEME_METADATA))
    raise ConfigError(
        "Unknown theme/template. Use a built-in theme "
        f"({allowed}) or pass an existing .css template path."
    )
