# Neksus JobSpec Skill (Gemini)

Help users create and repair valid Neksus JobSpec YAML.

## Focus

- Required top-level fields.
- Supported components only.
- Optional campaign metadata with valid status and dates.
- Method-based apply metadata only.
- Scope boundaries: no application forms, CV handling, payments,
  or hosted features.

## Local MCP

- Gemini CLI supports MCP server configuration.
- Use `neksus-jobspec-mcp` for local MCP integration when available.
- Use CLI and prompt-pack fallback in environments without MCP configuration access.
