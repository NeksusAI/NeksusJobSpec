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

### 3. Renderer/export layer

- Markdown, HTML, and JSON rendering
- Theme support for HTML rendering
- Schema export for editor/tooling integration

### 4. Docs site layer

- MkDocs + Material documentation
- Version-controlled Markdown docs
- GitHub Pages deployment workflow

## Local MCP architecture

### 5. Local MCP server

- Optional local stdio MCP server (`neksus-jobspec-mcp`)
- Wraps core validation/rendering/export/feed tooling as MCP tools
- Keeps local-first usage with no hosted deployment requirement

## Planned hosted/server architecture

### 6. Future hosted API (planned)

- Wrap core validation/rendering as networked services
- Expose stable contracts for organization-scale automation
- Keep schema/versioning explicit to reduce integration risk

## Design principles

- Keep CLI thin and core reusable
- Prefer explicit contracts over implicit behavior
- Preserve backward-compatible outputs where possible
- Avoid speculative complexity until needed
