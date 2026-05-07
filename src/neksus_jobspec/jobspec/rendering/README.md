# neksus_jobspec.jobspec.rendering

Rendering backend implementations and theme infrastructure.

## Purpose

Converts validated `JobSpec` models into presentation outputs.

## Main files

- `__init__.py`: rendering entrypoints and options wrappers.
- `html.py`: HTML construction and theme-context integration.
- `web.py`: web-format render adapter.
- `targets.py`: typed target models + renderers for JSON-LD, feeds, and sitemap XML.
- `normalize.py`: normalized payload helpers for rendering.
- `theme_engine.py`: package-based theme resolution and rendering.
- `themes.py`: theme metadata queries.

## Theme assets

- `theme_packages/*`: built-in theme package templates and manifests.
- `theme_css/*`: shared legacy CSS metadata assets (where still referenced).

## Target-Oriented Output Contracts

- JSON-LD output is built through a typed `JsonLdJobPosting` contract.
- Jobs feeds (`jobs-json`, `jobs-xml`) are built through typed feed target models before serialization.
- Sitemap XML is built through typed sitemap target models before serialization.

## Theme parity direction

Built-in and custom themes should converge on the same package/context contract.

## Phase 1 Contract

- Web rendering now builds a strict `ThemeRenderContext` from validated JobSpec YAML.
- Built-in and custom themes pass through the same pipeline:
  - context build
  - package validation (`manifest.json`, template, CSS, component/region compatibility)
  - Jinja render
- Theme presentation settings are centralized in `rendering.web.theme_config`.
- Users cannot define new component types; manifest component support must align with known schema components.
