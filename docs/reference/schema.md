# Schema

Neksus JobSpec v0.2.x uses a component-based schema (`schema_version: 1`).

## Breaking compatibility

v0.2.x is not backward compatible with legacy simple top-level content fields.

## Required fields

- `schema_version: int` (must be `1`)
- `id: str` (slug pattern)
- `page: object`
- `job: object`
- `components: list` (at least one component)

Optional:

- `rendering: object`

## Core nested blocks

```yaml
page:
  layout: job_detail
  language: da | en | ...
  theme: soft-professional
  component_order:
    - hero
    - facts

job:
  title: string
  intro: string | null
  apply:
    label: string
    url: string
```

## Validation behavior

- Missing required fields fail validation.
- Unknown component types fail validation.
- Unknown variants fail validation.
- Component IDs must be unique.
- `page.component_order`, when set, must include every component ID exactly once.

## Versioning

- Current supported version: `schema_version: 1`
- Other schema versions are rejected.
- Use `spec migrate` only for version inspection; write mode is not implemented.

See [Model Reference](model-reference.md) and [Specification](../concepts/specification.md).
