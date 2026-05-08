# AGENTS.md

Guidance for AI coding agents working in this repository.

## Owner-Maintained Policy

This repository is owner-maintained and does not use a public external contribution workflow.
Do not add generic language such as "Contributions are welcome."

## Product Boundary (Hard Rule)

Neksus JobSpec is a local-first Python package + CLI for structured, branded, machine-readable job campaign pages from YAML.

Allowed scope in free/core:
- local CLI
- local Python API
- local rendering/export/feed/sitemap
- assistant prompt packs in `skills/`
- optional local stdio MCP server

Out of scope:
- hosted SaaS/API infrastructure
- authentication/authorization
- database persistence
- application forms/candidate collection
- CV upload/parsing
- ATS workflow automation
- payments
- direct LinkedIn API posting

## First Priority Rules

Before marking work complete:
1. Update docs for user-visible behavior changes (`README.md`, docs under `docs/`, and relevant internal READMEs).
2. Update `CHANGELOG.md` for every user-visible change.
3. Keep temporary artifacts out of the commit.
4. Keep CLI and MCP thin; put orchestration in app/core services.

## Current Repository Layout

- `src/neksus_jobspec/`: core library
  - `jobspec/`: schema/models/parser/validator/rendering/exports/lint
  - `project/`: project config/discovery/checks/init
  - `app/`: use-case orchestration services (`SpecUseCase`, `RenderUseCase`, `FeedUseCase`, etc.)
- `src/neksus_jobspec_cli/`: Typer CLI entrypoint + command modules
- `src/neksus_jobspec_mcp/`: local stdio MCP server and MCP service adapters
- `examples/`: sample JobSpecs and theme examples
- `fixtures/`: test fixtures
- `tests/`: CLI/core/integration tests
- `docs/`: MkDocs documentation site

## Core Pipeline

```text
YAML -> parser/loader -> Pydantic JobSpec model -> app use cases -> render/export/feed/MCP/CLI
```

Rules:
- parser/validation/render/export logic belongs in core (`src/neksus_jobspec`).
- CLI command functions should only parse args, call use cases, and format output.
- MCP should map tool calls to the same app/core services.

## Schema and Compatibility Rules

- Do not change schema behavior silently.
- `schema_version` compatibility changes require:
  - explicit migration/compatibility notes
  - tests
  - docs updates
  - changelog entries
- Preserve stable JSON output shapes for machine-readable commands.

## Rendering/Export/Feed Rules

- Supported render formats: `web`, `json-ld`.
- Unknown render/export targets must fail with controlled errors.
- Export/feed/sitemap outputs should remain deterministic (ordering and stable structure).
- LinkedIn-ready export is a data profile only, not LinkedIn publishing.

## Changelog Governance

- `CHANGELOG.md` must be updated for every user-visible change.
- Add new release entries with grouped headings when preparing a release.
- Keep entries concise and factual.

## Commands and Entry Points

CLI:
- `neksus-jobspec` -> `neksus_jobspec_cli.main:app`

MCP:
- `neksus-jobspec-mcp` -> `neksus_jobspec_mcp.server:main`

## Required Quality Checks Before Finish

Run these when relevant changes were made:

```bash
python -m pip install -e .
python -m pip install -e ".[dev,mcp]"
neksus-jobspec --help
neksus-jobspec doctor
neksus-jobspec themes list
neksus-jobspec themes validate examples/themes/minimal
python -m pytest
uv run ruff check .
uv run ruff format --check .
python -m build
mkdocs build --strict
```

If a command cannot run in the current environment, document why in the final summary.

## Where to Edit What

- Schema/model behavior: `src/neksus_jobspec/jobspec/models.py`, `validator.py`, `schema.py`
- Rendering/themes: `src/neksus_jobspec/jobspec/rendering/`
- Export/feed/sitemap logic: `src/neksus_jobspec/jobspec/exports.py`, `src/neksus_jobspec/app/feed_service.py`
- App orchestration: `src/neksus_jobspec/app/`
- CLI commands: `src/neksus_jobspec_cli/commands/`
- MCP tool mapping/service: `src/neksus_jobspec_mcp/server.py`, `service.py`
- User docs: `README.md`, `docs/`
- LLM entry index: `llms.txt`
- Tests: `tests/`

## Simplicity and Surgical Changes

- Make minimal, direct changes tied to the requested behavior.
- Avoid speculative abstractions.
- Do not refactor unrelated areas.
- Remove only dead code introduced by your own edits.
