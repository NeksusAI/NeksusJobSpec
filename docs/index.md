# Neksus JobSpec

Neksus JobSpec is an open-source, local-first toolchain for writing, validating, inspecting, and rendering structured job specifications.

You write JobSpecs in YAML, validate them with stable model rules, and render them to formats like Markdown, HTML, and JSON.

## Why structured job specifications matter

Structured JobSpecs help teams:

- version and review role definitions in Git
- separate role content from presentation
- enforce consistent hiring requirements across teams
- reuse the same source for human docs and machine tooling

## Core value proposition

- Stable validation with explicit errors and warnings
- Deterministic rendering outputs
- CLI-first workflow with reusable core Python modules
- Schema export for editor and automation tooling

## Short example

```yaml
schema_version: 1
id: backend-engineer
title: Backend Engineer
summary: Build backend services for employer workflows.
responsibilities:
  - Design and implement backend APIs.
requirements:
  - 3+ years of backend software engineering experience.
```

Validate and render:

```bash
neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format markdown
```

## Next steps

- [Quickstart](quickstart.md)
- [Schema](schema.md)
- [Examples](examples.md)
- [MCP Server (planned)](mcp-server.md)
