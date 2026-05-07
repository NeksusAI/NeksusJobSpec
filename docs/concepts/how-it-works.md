# How It Works

Neksus JobSpec follows a simple pipeline:

```text
YAML input -> parse -> validate -> inspect -> render -> project check
```

## Pipeline stages

1. Parse: YAML files are loaded into dictionaries.
2. Validate: Pydantic validates dictionaries into typed `JobSpec` models.
3. Inspect: Metadata is extracted for human and JSON inspection outputs.
4. Render: Valid models render to web or json-ld outputs.
5. Check: Project-level checks validate config, directories, file validity, and duplicate IDs.

## Request lifecycle example

Input file `jobspecs/backend-engineer.jobspec.yaml`:

```bash
neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml --strict
```

Behavior:

- YAML is read and parsed.
- Model validation runs.
- Warning checks run (duplicates, short title, location detail checks).
- In `--strict`, warnings can fail the command.
- Output is emitted as human text or stable JSON (`--json`).

Then render:

```bash
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format web --theme soft-professional --output dist/backend-engineer.html
```

Behavior:

- Validated model is passed to renderer.
- Format-specific renderer outputs deterministic content.
- CLI writes output file if `--output` is provided.

## Boundaries

- CLI layer: thin command orchestration and output formatting.
- Core layer: parsing, validation, checks, and rendering logic.
- Local MCP layer: optional local stdio server wrapping core logic.
- Hosted API: future network wrappers beyond local tooling; not implemented now.
