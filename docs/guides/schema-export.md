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

## Stability notes

- Schema is generated from `JobSpec` Pydantic model.
- Current schema version is `1`.
- Versioned schema artifact convention: `schemas/jobspec.v1.json`.
