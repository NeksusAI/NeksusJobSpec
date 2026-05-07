# MCP Install Matrix

This matrix documents practical local setup paths for Claude, ChatGPT, Gemini, and Copilot.

The Neksus MCP server itself is local stdio:

```bash
neksus-jobspec-mcp
```

Install dependency extra first:

```bash
pip install "neksus-jobspec[mcp]"
```

## Claude

Direct local MCP is supported in Claude Desktop.

Use your Claude MCP/local server config to run:

- command: `neksus-jobspec-mcp`
- args: `[]`

Reference: Anthropic local MCP setup docs.
[Anthropic: local MCP on Claude Desktop](https://support.anthropic.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop)

## ChatGPT

ChatGPT supports MCP through custom connectors/developer mode flows, but local process wiring can vary by plan/workspace and product surface.

Recommended path:

1. Use MCP connector workflow where available.
2. If direct local process wiring is unavailable in your environment, use:
   - the Neksus CLI locally, and
   - the ChatGPT prompt pack in `skills/chatgpt/`.

Reference: OpenAI MCP and connectors documentation.
[OpenAI: MCP docs](https://platform.openai.com/docs/mcp/) and [OpenAI Help: connectors in ChatGPT](https://help.openai.com/en/articles/11487775/)

## Gemini

Gemini CLI supports MCP server configuration, including stdio command-based servers.

Configure your Gemini MCP settings to launch:

- command: `neksus-jobspec-mcp`
- args: `[]`

If your Gemini environment does not expose MCP config controls, use CLI + prompt-pack fallback (`skills/gemini/`).

Reference: Gemini CLI MCP documentation.
[Gemini CLI MCP docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md)

## Copilot

Copilot MCP capability depends on editor/client and policy controls (especially in Business/Enterprise contexts).

When MCP server configuration is available, point it to:

- command: `neksus-jobspec-mcp`
- args: `[]`

If local MCP server configuration is not available in your Copilot environment, use CLI + prompt-pack fallback (`skills/copilot/`).

Reference: GitHub MCP docs for Copilot.
[GitHub Docs: About MCP in Copilot](https://docs.github.com/copilot/concepts/context/mcp)

## Fallback path (all assistants)

When direct MCP wiring is unavailable:

1. Run `neksus-jobspec` commands locally.
2. Use assistant prompt packs under `skills/`.
3. Keep workflows local-first with validated YAML and deterministic exports.
