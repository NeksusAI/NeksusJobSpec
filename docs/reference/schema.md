# Schema

Neksus JobSpec v0.4.x uses `schema_version: 1` with component-based composition.

## Required fields

- `schema_version: 1`
- `id: slug string`
- `page: object`
- `job: object`
- `components: non-empty list`

Optional:
- `campaign`
- `rendering`

## Key nested fields

```yaml
job:
  title: string
  intro: string | null
  apply:
    method: email | external_url | ats_url | custom | agent_ready
    email: string | null
    url: string | null
    job_reference: string | null

campaign:
  starts_at: YYYY-MM-DD | null
  expires_at: YYYY-MM-DD | null
  status: draft | active | expired | closed | null
```

## Validation behavior

- Unknown fields are rejected.
- Unknown component types/variants are rejected.
- Duplicate component IDs are rejected.
- `page.component_order` must include all component IDs exactly once if set.
- `campaign.expires_at` must be >= `campaign.starts_at` when both are set.
- apply methods enforce method-specific required fields.

## Related commands

```bash
neksus-jobspec spec schema --output schemas/jobspec.v1.json
neksus-jobspec spec validate <path>
neksus-jobspec spec lint <path>
```

See [Model Reference](model-reference.md) for model-level details.
