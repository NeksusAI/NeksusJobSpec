# Local MCP Server

Neksus JobSpec includes an optional local-only stdio MCP server.

It is designed to run on your machine and expose JobSpec tooling to
MCP-capable assistants. It does not add hosted deployment behavior.

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

The server uses stdio transport and is intended to be launched by your MCP
client.

## Tool surface

The local MCP server exposes CLI-parity-oriented tools:

- `version`
- `init`
- `check`
- `config_get`
- `config_set`
- `themes_list`
- `themes_show`
- `spec_schema`
- `spec_templates`
- `spec_new`
- `spec_validate`
- `spec_render`
- `spec_inspect`
- `spec_status`
- `spec_migrate`
- `spec_export`
- `feed_export`
- `feed_sitemap`

All tool responses use stable JSON payloads with `ok` and explicit error
payloads on failures.

## Scope boundary

The MCP server is local-only and free/core scoped.

It does not implement:

- application collection
- `application_form` schema handling
- CV upload/parsing
- candidate management
- email delivery
- payments
- direct LinkedIn posting
- hosted APIs or cloud service orchestration

See [MCP Install Matrix](mcp-install-matrix.md) for Claude, ChatGPT, Gemini,
and Copilot setup paths.
