# Architecture

Neksus JobSpec is structured as a reusable local-first core with thin interfaces.

## Runtime layers

1. CLI layer (`neksus-jobspec`)
- argument parsing
- human/json output formatting
- thin delegation to app use cases

2. Core app/use-case layer (`neksus_jobspec.app`)
- orchestrates validate/render/export/feed/project flows
- shared by CLI and MCP

3. Domain layer (`neksus_jobspec.jobspec`)
- parser, Pydantic models, validation, rendering, exports, lint

4. Project layer (`neksus_jobspec.project`)
- project discovery, config, checks, initialization

5. MCP adapter layer (`neksus_jobspec_mcp`)
- local stdio tools mapped to the same core use cases

## Pipeline

```text
YAML -> parser/loader -> Pydantic JobSpec model -> app use cases -> render/export/feed/MCP/CLI
```

## Principle

Keep CLI and MCP thin; place behavior and orchestration in core services.
