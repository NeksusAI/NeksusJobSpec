# Assistant Usage

## Source of truth

Neksus JobSpec YAML is the source of truth. Assistants should not invent schema fields or skip validation.

## Recommended assistant flow

1. Load or generate YAML.
2. Validate before rendering or transforming.
3. Use JSON output for automation.
4. Use Markdown or HTML output for human review.

## CLI examples

Validate a JobSpec:

```bash
neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml
```

Render Markdown for chat/review:

```bash
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format markdown
```

Render JSON for automation:

```bash
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format json --json
```

## Python API example

```python
from neksus_jobspec import load_jobspec, render_jobspec, validate_jobspec

spec = load_jobspec("jobspecs/backend-engineer.jobspec.yaml")
validated = validate_jobspec(spec.model_dump())
json_output = render_jobspec(validated, format="json")
```

## Current boundaries

- Local-first package and CLI: available now
- Hosted API: planned, not implemented
- MCP server: planned, not implemented
