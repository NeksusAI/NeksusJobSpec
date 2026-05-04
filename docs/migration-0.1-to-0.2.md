# Migration: 0.1.0 to 0.2.x

`0.2.x` is a breaking schema/model update.

## What changed

- Legacy top-level content fields are no longer the primary schema.
- Job pages must use:
  - `job`
  - `components`
  - optional `rendering`
- Render formats are `web` and `json-ld`.

## Practical migration steps

1. Move role content into `job.title`, `job.intro`, and typed components.
2. Replace old free-form sections with component types:
   - summary/body -> `rich_text`
   - requirements/responsibilities -> `list` / `feature_grid`
   - side facts -> `meta_panel`
   - map/location -> `location_map`
3. Add explicit `page.component_order`.
4. Validate:

```bash
neksus-jobspec spec validate path/to/spec.jobspec.yaml --strict
```

5. Render and compare:

```bash
neksus-jobspec spec render path/to/spec.jobspec.yaml --format web --theme soft-professional
```

## Recommended baseline

Start from:

- `examples/job-detail.jobspec.yaml`

Then adapt content incrementally.
