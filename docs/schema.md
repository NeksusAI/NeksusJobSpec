# Schema

Neksus JobSpec uses a Pydantic v2 model with `schema_version: 1`.

## Current fields and types

Required fields:

- `schema_version: int` (must be `1`)
- `id: str` (slug format)
- `title: str`
- `summary: str`
- `responsibilities: list[str]` (at least one non-empty item)
- `requirements: list[str]` (at least one non-empty item)

Optional fields:

- `department: str | null`
- `level: str | null`
- `location: Location | null`
- `nice_to_have: list[str]` (defaults to `[]`, non-empty strings when present)
- `employment: Employment | null`

Nested types:

```yaml
location:
  type: remote | hybrid | onsite
  city: string | null
  country: string | null

employment:
  type: full-time | part-time | contract | internship
```

## Validation behavior

- Missing required fields fail validation.
- Optional fields may be omitted.
- Validation warnings are separate from hard validation errors.

Warnings include:

- very short title
- duplicate responsibilities
- duplicate requirements
- hybrid/onsite role missing both city and country

Use strict mode to treat warnings as failures:

```bash
neksus-jobspec spec validate jobspecs/example.jobspec.yaml --strict
neksus-jobspec check --strict
```

## Versioning and compatibility

- Current supported version: `schema_version: 1`
- Other schema versions are rejected by the current validator.
- Migration surface exists via `neksus-jobspec spec migrate` for future transitions.
- Validation and project-check outputs use stable issue/result shapes.

For full field-by-field constraints, see [Model Reference](model-reference.md).
For editor wiring and schema export workflows, see [Schema Editor Integration](schema-editor-integration.md).
