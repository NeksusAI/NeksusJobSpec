# Schema Editor Integration

Use JSON Schema export to provide YAML autocompletion and validation in editors.

## Export schema

```bash
neksus-jobspec spec schema --output schemas/jobspec.v1.json
```

Or print JSON payload mode:

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

With `--output` + `--json`:

```json
{
  "ok": true,
  "format": "json-schema",
  "schema_version": 1,
  "output": "schemas/jobspec.v1.json"
}
```

## VS Code YAML integration example

Add to `.vscode/settings.json`:

```json
{
  "yaml.schemas": {
    "./schemas/jobspec.v1.json": "jobspecs/*.jobspec.yaml"
  }
}
```

## Schema version compatibility

- Current supported value is `schema_version: 1`.
- Other schema versions are rejected by current validators.
- Regenerate schema when model constraints change.

For model details, see [Model Reference](model-reference.md).
