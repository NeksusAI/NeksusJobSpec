# Schema

Neksus JobSpec v0.3.x uses a component-based schema (`schema_version: 1`).

## Breaking compatibility

v0.3.x is not backward compatible with legacy simple top-level content fields.

## Required fields

- `schema_version: int` (must be `1`)
- `id: str` (slug pattern)
- `page: object`
- `job: object`
- `components: list` (at least one component)

Optional:

- `campaign: object`
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
    method: email | external_url | ats_url | custom | agent_ready
    label: string | null
    email: string | null
    url: string | null
    job_reference: string | null

campaign:
  starts_at: YYYY-MM-DD | null
  expires_at: YYYY-MM-DD | null
  status: draft | active | expired | closed | null
```

## Validation behavior

- Missing required fields fail validation.
- Unknown component types fail validation.
- Unknown variants fail validation.
- Component IDs must be unique.
- `page.component_order`, when set, must include every component ID exactly once.
- `campaign.expires_at` must not be before `campaign.starts_at`.
- `job.apply` must satisfy method-specific required fields.

## Versioning

- Current supported version: `schema_version: 1`
- Other schema versions are rejected.
- Use `spec migrate` only for version inspection; write mode is not implemented.

See [Model Reference](model-reference.md) and [Specification](../concepts/specification.md).
