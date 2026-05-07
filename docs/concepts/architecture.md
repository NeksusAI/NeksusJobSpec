# Architecture

Neksus JobSpec is intentionally split into simple layers to keep open-source usage clean while enabling future hosted/server products.

## Current open-source architecture

### 1. CLI/package layer

- `neksus-jobspec` Typer commands
- Human and JSON command outputs
- Thin orchestration over core modules

### 2. Schema/validation layer

- Pydantic v2 models for JobSpec
- Parse and validation normalization
- Structured errors and warnings

### 3. Application use-case layer

- Core orchestration use cases under `neksus_jobspec.app`
- Reusable spec/project/feed workflows shared by CLI and MCP
- Typed DTO payloads for app-layer contracts
- Shared `ProjectContext` for root/config discovery in project workflows
- Shared filesystem gateway for app-layer side effects

### 4. JobSpec operation layer

- Vertical slices under `neksus_jobspec.jobspec.spec_ops`
- File-oriented operations grouped by use case (`new`, `validate`, `render`, `inspect`, `export`, `migrate`)
- Thin wrappers around stable domain modules in `neksus_jobspec.jobspec`

### 5. Renderer/export layer

- Markdown, HTML, and JSON rendering
- Theme support for HTML rendering
- Schema export for editor/tooling integration

### 6. Docs site layer

- MkDocs + Material documentation
- Version-controlled Markdown docs
- GitHub Pages deployment workflow

## Local MCP architecture

### 7. Local MCP server

- Optional local stdio MCP server (`neksus-jobspec-mcp`)
- Wraps core validation/rendering/export/feed tooling as MCP tools
- Keeps local-first usage with no hosted deployment requirement

## Planned hosted/server architecture

### 8. Future hosted API (planned)

- Wrap core validation/rendering as networked services
- Expose stable contracts for organization-scale automation
- Keep schema/versioning explicit to reduce integration risk

## Design principles

- Keep CLI thin and core reusable
- Prefer explicit contracts over implicit behavior
- Preserve backward-compatible outputs where possible
- Avoid speculative complexity until needed
