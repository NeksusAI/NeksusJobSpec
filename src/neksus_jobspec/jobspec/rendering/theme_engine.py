"""Theme package loading and Jinja rendering."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from neksus_jobspec.errors import ConfigError, FileSystemError
from neksus_jobspec.jobspec.rendering.theme_contract import (
    GLOBAL_MANDATORY_COMPONENT_TYPES,
    ThemeRenderContext,
)

_BUILTIN_THEME_IDS = {"soft-professional", "classic", "classic-dark"}
_ALLOWED_COMPONENTS = {
    "hero",
    "facts",
    "rich_text",
    "list",
    "quote",
    "benefits",
    "contact",
    "company_profile",
    "legal",
    "cta",
    "media",
    "application_process",
    "header_brand",
    "hero_banner",
    "meta_panel",
    "social_links",
    "location_map",
    "footer_brand",
    "nav_links",
    "header_actions",
    "feature_grid",
    "meta_chips",
}
_ALLOWED_REGIONS = {"header", "hero", "main", "sidebar", "footer"}


class ThemeManifest(BaseModel):
    """Theme package manifest schema."""

    model_config = ConfigDict(extra="forbid")

    name: str
    version: int = 1
    template: str = "template.html.j2"
    styles: list[str] = Field(default_factory=list)
    supported_components: list[str] = Field(default_factory=list)
    supported_regions: list[str] = Field(default_factory=list)
    required_components: list[str] = Field(default_factory=list)


@dataclass(frozen=True)
class ThemePackage:
    """Resolved theme package files."""

    theme_id: str
    root: Path
    manifest: ThemeManifest


def builtin_theme_root() -> Path:
    return Path(__file__).with_name("theme_packages")


def load_manifest(theme_root: Path) -> ThemeManifest:
    manifest_path = theme_root / "manifest.json"
    if not manifest_path.exists():
        raise ConfigError(f"Missing theme manifest: {manifest_path}")
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise FileSystemError(f"Failed to read theme manifest: {manifest_path}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigError(f"Invalid JSON in theme manifest: {manifest_path}") from exc

    try:
        manifest = ThemeManifest.model_validate(payload)
    except ValidationError as exc:
        raise ConfigError(f"Theme manifest is invalid: {manifest_path}") from exc

    unknown_components = sorted(set(manifest.supported_components) - _ALLOWED_COMPONENTS)
    if unknown_components:
        raise ConfigError(
            "Theme manifest includes unknown components: " + ", ".join(unknown_components)
        )

    unknown_regions = sorted(set(manifest.supported_regions) - _ALLOWED_REGIONS)
    if unknown_regions:
        raise ConfigError("Theme manifest includes unknown regions: " + ", ".join(unknown_regions))

    template_path = theme_root / manifest.template
    if not template_path.exists():
        raise ConfigError(f"Theme template file does not exist: {template_path}")

    for css_file in manifest.styles:
        css_path = theme_root / css_file
        if not css_path.exists():
            raise ConfigError(f"Theme CSS file does not exist: {css_path}")

    return manifest


def resolve_theme_package(theme_value: str, template_hint: str | None = None) -> ThemePackage:
    key = theme_value.strip()
    if not key:
        raise ConfigError("Theme value must not be empty")

    if key in _BUILTIN_THEME_IDS:
        root = builtin_theme_root() / key
        return ThemePackage(theme_id=key, root=root, manifest=load_manifest(root))

    if key == "custom":
        if not template_hint:
            raise ConfigError("Theme 'custom' requires rendering.web.template path")
        custom_root = Path(template_hint).expanduser()
        if not custom_root.is_absolute():
            custom_root = (Path.cwd() / custom_root).resolve()
        if not custom_root.exists() or not custom_root.is_dir():
            raise ConfigError(f"Custom theme path must be an existing directory: {custom_root}")
        return ThemePackage(
            theme_id="custom", root=custom_root, manifest=load_manifest(custom_root)
        )

    as_path = Path(key).expanduser()
    if not as_path.is_absolute():
        as_path = (Path.cwd() / as_path).resolve()
    if as_path.exists() and as_path.is_dir():
        return ThemePackage(theme_id="custom", root=as_path, manifest=load_manifest(as_path))

    allowed = ", ".join(sorted(_BUILTIN_THEME_IDS | {"custom"}))
    raise ConfigError(
        f"Unknown theme: {key}. Use one of: {allowed}, or pass a theme directory path."
    )


def render_theme(
    package: ThemePackage, context: dict[str, Any], custom_css: str | None = None
) -> str:
    """Render HTML for a resolved theme package."""
    env = Environment(
        loader=FileSystemLoader(str(package.root)),
        autoescape=select_autoescape(enabled_extensions=("html", "xml", "j2")),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    css_chunks: list[str] = []
    for css_file in package.manifest.styles:
        css_path = package.root / css_file
        try:
            css_chunks.append(css_path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise FileSystemError(f"Failed to read theme CSS file: {css_path}") from exc

    if custom_css:
        css_chunks.append(custom_css.strip())

    template = env.get_template(package.manifest.template)
    return template.render(**context, theme_css="\n".join(chunk for chunk in css_chunks if chunk))


def validate_theme_package(package: ThemePackage, context: ThemeRenderContext) -> None:
    """Validate package-to-context compatibility using the shared render contract."""
    manifest = package.manifest

    supported = set(manifest.supported_components)
    required = set(manifest.required_components or GLOBAL_MANDATORY_COMPONENT_TYPES)
    required_missing = sorted(required - supported)
    if required_missing:
        raise ConfigError(
            "Theme manifest must support mandatory components: " + ", ".join(required_missing)
        )

    context_types = {component.type for component in context.components}
    unsupported = sorted(context_types - supported)
    if unsupported:
        raise ConfigError(
            "Theme manifest does not support component types used by this JobSpec: "
            + ", ".join(unsupported)
        )

    supported_regions = set(manifest.supported_regions)
    context_regions = {component.region for component in context.components}
    unsupported_regions = sorted(context_regions - supported_regions)
    if unsupported_regions:
        raise ConfigError(
            "Theme manifest does not support regions used by this JobSpec: "
            + ", ".join(unsupported_regions)
        )
