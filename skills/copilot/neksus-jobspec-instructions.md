# Neksus JobSpec Instructions (Copilot)

Generate valid Neksus JobSpec YAML and related Python/CLI changes.

## Constraints

- Keep schema-compatible output.
- Apply metadata is destination-only (no application forms).
- Never invent unsupported fields.
- Never claim direct platform posting support.
- Prefer deterministic exports and stable CLI output.

## Local MCP

- If your Copilot environment exposes MCP server configuration,
  point it to `neksus-jobspec-mcp`.
- If MCP server wiring is unavailable in your environment,
  use CLI commands and this instruction pack.
