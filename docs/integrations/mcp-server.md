# MCP Server (Planned)

This page describes the intended MCP/server direction. It is planned, not currently implemented.

## Why MCP for JobSpec

MCP clients typically need a running server process that can expose tools and structured resources. For Neksus JobSpec, this would let AI clients request schema info, validate specs, and generate outputs from a single source of truth.

## Intended server responsibilities

- Expose JobSpec schema and version metadata
- Validate JobSpec documents
- Generate/export Markdown, HTML, and JSON outputs
- Provide reusable templates and examples
- Support LLM clients through stable tool contracts

## Proposed tool surface

- `get_schema`
- `validate_jobspec`
- `render_jobspec`
- `list_templates`
- `convert_to_format`

## Status

Current repository status:

- CLI and reusable Python core: available now
- MCP server process: planned
- Hosted API deployment: planned
