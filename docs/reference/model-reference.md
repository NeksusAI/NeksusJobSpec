# Model Reference

This page documents the v0.2.0 component-based `JobSpec` model (`schema_version: 1`).

## Top-level model: `JobSpec`

- `schema_version: int = 1`
- `id: str` (pattern `^[a-z0-9]+(?:-[a-z0-9]+)*$`)
- `page: PageConfig`
- `job: JobConfig`
- `components: list[Component]` (min length 1)
- `rendering: RenderingConfig` (optional with defaults)

## `PageConfig`

- `layout: "job_detail"`
- `language: str | None`
- `theme: str | None`
- `component_order: list[str]`

## `JobConfig`

- `title: str` (required)
- `intro: str | None`
- `apply: {label: str, url: str} | None`

## Components

Supported `type` values:

- `hero`, `facts`, `rich_text`, `list`, `quote`, `benefits`, `contact`, `company_profile`, `legal`, `cta`, `media`, `application_process`

Shared fields:

- `type`, `id`, optional `variant`, `title`, `class_name`, `attributes`, `visibility`, `render_if`

## Validation rules

- component IDs must be unique
- unknown type/variant fails
- `page.component_order` entries must match existing component IDs
- `schema_version` must be `1`
