# JobSpec Format

Neksus v0.4.x uses a component-based JobSpec schema (`schema_version: 1`).

## Compatibility note

Legacy simple-schema top-level content formats are not supported.

## Required top-level fields

- `schema_version` (must be `1`)
- `id`
- `page`
- `job`
- `components`

Optional:
- `campaign`
- `rendering`

## Campaign metadata

```yaml
campaign:
  starts_at: 2026-05-04
  expires_at: 2026-07-03
  status: active
```

Rules:
- `status` is `draft | active | expired | closed`.
- `expires_at` cannot be before `starts_at`.

## Apply destination

`job.apply` is method-based:

- `email` -> requires `email`
- `external_url` -> requires `url`
- `ats_url` -> requires `url`
- `custom` -> requires `url`
- `agent_ready` -> requires `url` and `job_reference`

## Validation and lint

- `spec validate` enforces schema validity and exits non-zero on invalid specs.
- `spec lint` reports advisory quality warnings without failing valid specs.
- `spec status` reports campaign metadata plus quality warnings.

## Components

Common fields include `type`, `id`, optional `variant`, optional `title`, and placement/region-related fields.

Key rules:
- component IDs must be unique
- when `page.component_order` is set, it must include all component IDs exactly once
- unknown component types/variants fail validation

## Rendering fields

`rendering.web` supports:
- `template`
- `theme_config`
- `labels`
- `asset_base_url`
- behavior flags like `show_top_apply`, `show_share_links`, `show_print_link`, `repeat_cta`

See [Schema](../reference/schema.md) for reference and [Themes](themes.md) for package behavior.
