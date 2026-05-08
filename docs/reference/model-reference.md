# Model Reference

This page summarizes the component-based `JobSpec` model used in v0.4.x.

## Top-level `JobSpec`

- `schema_version: int = 1`
- `id: slug string`
- `page: PageConfig`
- `job: JobConfig`
- `campaign: CampaignConfig | None`
- `components: list[Component]` (min length 1)
- `rendering: RenderingConfig`

## Key nested blocks

- `PageConfig`: layout/language/theme/component order metadata
- `JobConfig`: job title/intro + apply destination metadata
- `CampaignConfig`: optional start/end/status metadata
- `JobApply`: method-based apply destination contract

## Validation highlights

- schema version must be `1`
- component IDs must be unique
- unknown component types/variants fail
- `page.component_order` must match all components exactly once when set
- campaign date ordering is enforced
- method-specific apply fields are enforced

For exact JSON Schema, use:

```bash
neksus-jobspec spec schema --output schemas/jobspec.v1.json
```
