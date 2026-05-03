# Integrations

This page separates what is available now from planned integration paths.

## Available now

### ChatGPT, Claude, Gemini, GitHub Copilot

You can use Neksus JobSpec as a local structured source of truth:

- keep role specs in YAML under version control
- validate specs before sharing with LLM tools
- render to Markdown/JSON for prompt context or review flows

### CI/CD

You can run CLI checks in CI to enforce quality gates:

```bash
uv sync
uv run neksus-jobspec check --strict
uv run pytest
```

## Planned integrations

### ATS and job-board pipelines (planned)

Planned direction is to map validated JobSpec fields into ATS/job-board payloads and export adapters. This is not implemented in the current CLI.

### Hosted API/server workflows (planned)

Planned direction is to expose the same core validation/rendering logic behind a hosted API for team-wide automation.
