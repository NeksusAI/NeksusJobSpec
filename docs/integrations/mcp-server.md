# Local MCP Server

Neksus JobSpec includes a local-only stdio MCP server.

It is designed for running on your own machine and exposing JobSpec tooling to MCP-capable assistants.
It does not add hosted deployment behavior.

## Install

```bash
pip install "neksus-jobspec[mcp]"
```

Using `uv`:

```bash
uv sync --extra mcp
```

## Run

```bash
neksus-jobspec-mcp
```

The server uses stdio transport and is intended to be launched by your MCP client.

## Tool surface

The local MCP server exposes CLI-parity-oriented tools, including:

- `version`, `init`, `check`
- `config_get`, `config_set`
- `themes_list`, `themes_show`
- `spec_schema`, `spec_templates`, `spec_new`
- `spec_validate`, `spec_render`, `spec_inspect`, `spec_status`, `spec_migrate`, `spec_export`
- `feed_export`, `feed_sitemap`

All tool responses use stable JSON payloads with `ok` and explicit error payloads when failures occur.

## Scope boundary

- Local-only tooling.
- No hosted API behavior.
- No application intake, CV handling, payments, or commercial SaaS functionality.

See [MCP Install Matrix](mcp-install-matrix.md) for Claude, ChatGPT, Gemini, and Copilot setup paths.
