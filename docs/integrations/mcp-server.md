# Local MCP Server

Neksus JobSpec includes an optional local-only stdio MCP server.

## Install

```bash
pip install "neksus-jobspec[mcp]"
```

## Run

```bash
neksus-jobspec-mcp
```

## Tool surface

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
- `spec_lint`
- `spec_render`
- `spec_inspect`
- `spec_status`
- `spec_migrate`
- `spec_export`
- `feed_export`
- `feed_sitemap`

All responses use stable JSON payloads with explicit failure payloads.

## Scope boundary

Local MCP is local-only tooling parity. It does not add hosted SaaS, ATS/candidate workflows, payments, auth, or direct LinkedIn posting.
