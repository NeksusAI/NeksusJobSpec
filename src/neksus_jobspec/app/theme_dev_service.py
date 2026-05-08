"""Theme development helper service for CLI workflows."""

from __future__ import annotations

import json
from pathlib import Path

from neksus_jobspec.jobspec.models import JobSpec
from neksus_jobspec.jobspec.renderer import render_jobspec
from neksus_jobspec.jobspec.rendering import get_theme_metadata, list_theme_metadata
from neksus_jobspec.jobspec.rendering.theme_engine import load_manifest, resolve_theme_package

_MINIMAL_SPEC = {
    "schema_version": 1,
    "id": "theme-validation-sample",
    "page": {"layout": "job_detail"},
    "job": {
        "title": "Theme Validation Sample",
        "apply": {"method": "external_url", "url": "https://example.com/apply"},
    },
    "components": [
        {
            "type": "hero",
            "id": "hero",
            "title": "Theme Validation Sample",
            "intro": "Intro text",
        },
        {
            "type": "list",
            "id": "requirements",
            "items": ["One item"],
        },
    ],
}


class ThemeDevService:
    """Service for theme listing, inspection, validation, and scaffolding."""

    def list_themes(self) -> list[dict[str, object]]:
        themes = []
        for item in list_theme_metadata():
            payload = item.model_dump()
            payload["source"] = "built-in"
            themes.append(payload)
        return themes

    def show_theme(self, value: str) -> dict[str, object]:
        as_path = Path(value).expanduser()
        if as_path.exists() and as_path.is_dir():
            package = resolve_theme_package(str(as_path.resolve()))
            manifest = package.manifest
            return {
                "name": manifest.name,
                "source": "filesystem/custom",
                "path": str(package.root),
                "version": manifest.version,
                "description": "Custom filesystem theme package",
                "templates": [manifest.template],
                "assets": manifest.styles,
                "supported_components": manifest.supported_components,
                "supported_regions": manifest.supported_regions,
            }

        built_in = get_theme_metadata(value).model_dump()
        return {
            "name": built_in["name"],
            "source": "built-in",
            "version": None,
            "description": built_in["description"],
            "templates": ["template.html.j2"],
            "assets": [f"{built_in['name']}.css"],
            "supported_formats": built_in["supported_formats"],
            "layout_notes": built_in["layout_notes"],
            "token_hints": built_in["token_hints"],
        }

    def validate_theme_path(self, theme_path: Path) -> dict[str, object]:
        theme_root = theme_path.resolve()
        manifest = load_manifest(theme_root)
        spec = JobSpec.model_validate(_MINIMAL_SPEC)
        render_jobspec(spec, format="web", theme=str(theme_root))
        return {
            "ok": True,
            "path": str(theme_root),
            "name": manifest.name,
            "template": manifest.template,
            "styles": manifest.styles,
        }

    def init_theme(self, target: Path, force: bool = False) -> dict[str, object]:
        root = target.resolve()
        if root.exists() and any(root.iterdir()) and not force:
            raise ValueError("Target directory is not empty. Use --force to overwrite.")
        root.mkdir(parents=True, exist_ok=True)

        manifest = {
            "name": root.name,
            "version": 1,
            "template": "template.html.j2",
            "styles": ["theme.css"],
            "supported_components": [
                "hero",
                "list",
                "benefits",
                "contact",
                "cta",
                "legal",
            ],
            "supported_regions": ["header", "hero", "main", "sidebar", "footer"],
            "required_components": ["hero", "list"],
        }

        (root / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        (root / "template.html.j2").write_text(
            """<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>{{ title }}</title>
    <style>{{ theme_css }}</style>
  </head>
  <body>
    <main class=\"page\">
      <h1>{{ title }}</h1>
      {% for component in components %}
      <section id=\"{{ component.id }}\">
        {% if component.title %}<h2>{{ component.title }}</h2>{% endif %}
        {% if component.type == \"list\" %}
        <ul>
          {% for item in component.items %}<li>{{ item }}</li>{% endfor %}
        </ul>
        {% endif %}
      </section>
      {% endfor %}
    </main>
  </body>
</html>
""",
            encoding="utf-8",
        )
        (root / "theme.css").write_text(
            """body { font-family: ui-sans-serif, system-ui, sans-serif; margin: 0; }
.page { max-width: 860px; margin: 0 auto; padding: 32px 20px; }
h1 { margin: 0 0 20px; }
section { margin: 16px 0; }
""",
            encoding="utf-8",
        )
        (root / "README.md").write_text(
            """# Minimal Theme

This is a minimal custom theme package scaffold.

Validate with:

```bash
neksus-jobspec themes validate .
```
""",
            encoding="utf-8",
        )
        return {"ok": True, "path": str(root)}
