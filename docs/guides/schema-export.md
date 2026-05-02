# Schema Export

`neksus-jobspec` can export a versioned JSON Schema for editor tooling.

## Command

```bash
neksus-jobspec spec schema
```

## Write to file

```bash
neksus-jobspec spec schema --output schemas/jobspec.v1.json
```

## JSON mode

```bash
neksus-jobspec spec schema --json
```

JSON mode shape:

```json
{
  "ok": true,
  "format": "json-schema",
  "schema_version": 1,
  "schema": {}
}
```

When `--output` is used with `--json`, payload includes:

```json
{
  "ok": true,
  "format": "json-schema",
  "schema_version": 1,
  "output": "schemas/jobspec.v1.json"
}
```

## Stability notes

- Schema is generated from `JobSpec` Pydantic model.
- Current schema version is `1`.
- Versioned schema artifact convention: `schemas/jobspec.v1.json`.
