# neksus_jobspec.jobspec.rendering

Rendering backend implementations and theme infrastructure.

## Purpose

Converts validated `JobSpec` models into presentation outputs.

## Main files

- `__init__.py`: rendering entrypoints and options wrappers.
- `html.py`: HTML construction and theme-context integration.
- `web.py`: web-format render adapter.
- `json_ld.py`: JSON-LD formatter.
- `normalize.py`: normalized payload helpers for rendering.
- `theme_engine.py`: package-based theme resolution and rendering.
- `themes.py`: theme metadata queries.

## Theme assets

- `theme_packages/*`: built-in theme package templates and manifests.
- `theme_css/*`: built-in CSS assets.

## Theme parity direction

Built-in and custom themes should converge on the same package/context contract.
