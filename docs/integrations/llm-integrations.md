# Integrations

## Available now

- Local YAML-first workflow under version control.
- CLI validation/lint/render/export/feed/sitemap.
- Optional local MCP server for MCP-capable assistants.

## Typical LLM integration pattern

- generate/update JobSpec YAML
- run `spec validate` and `spec lint`
- render/export deterministic outputs
- review artifacts before publishing in external systems

## MCP

- Install: `pip install "neksus-jobspec[mcp]"`
- Run: `neksus-jobspec-mcp`
- Setup matrix: [MCP Install Matrix](mcp-install-matrix.md)

## Out of scope

Hosted ATS-like workflows and direct posting integrations are not part of the local core package.
