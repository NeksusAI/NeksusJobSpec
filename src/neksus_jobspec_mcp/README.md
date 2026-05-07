# neksus_jobspec_mcp

Local stdio MCP server package for Neksus JobSpec.

## Purpose

Expose CLI-parity operations as MCP tools for local assistants and automation.

## Files

- `server.py`: MCP server entrypoint and tool registration.
- `service.py`: tool handlers that delegate to app-layer use cases.

## Rule

MCP handlers should remain thin, deterministic, and aligned with CLI behavior and error codes.
