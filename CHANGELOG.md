# Changelog

All notable user-visible changes to this project are documented in this file.

The format is inspired by Keep a Changelog and follows Semantic Versioning.

## [Unreleased]

### Added
- Optional local stdio MCP server executable: `neksus-jobspec-mcp`.
- Optional dependency extra for MCP runtime: `neksus-jobspec[mcp]`.
- MCP service tool surface for local workflows:
  - project/config/check operations
  - spec schema/template/new/validate/render/inspect/status/migrate/export
  - feed export and sitemap generation
- MCP integration docs and assistant install matrix for Claude, ChatGPT, Gemini, and Copilot.

### Changed
- Integrations and architecture docs now describe local MCP as available.

## [0.3.0]

### Added
- Optional `campaign` metadata (`starts_at`, `expires_at`, `status`) with schema validation.
- New apply destination metadata with method-based contract:
  - `email`, `external_url`, `ats_url`, `custom`, `agent_ready`
- Single-job exports via `neksus-jobspec spec export`:
  - `generic-json`
  - `generic-xml`
  - `linkedin-ready-json`
- Multi-job feeds via `neksus-jobspec feed export`:
  - `jobs-json`
  - `jobs-xml`
- Sitemap generation via `neksus-jobspec feed sitemap`.
- Optional assistant prompt packs in `skills/` for ChatGPT, Claude, Copilot, and Gemini.
- New examples for campaign/apply/export workflows.

### Changed
- BREAKING: `job.apply` no longer accepts legacy `{label, url}` shape.
- JSON-LD `validThrough` now maps from `campaign.expires_at` when provided.
- Web rendering shows a visible closed/expired campaign notice.
- Version bumped to `0.3.0`.

### Deferred
- Additional built-in visual themes remain deferred for a later phase.
- Hosted/commercial features remain out of scope for the free/core package.

## [0.2.0]

### Added
- Controlled composable job-detail page components.
- Structured validation and project checks for component-based specs.
- Built-in `soft-professional` web theme.
- Public Python API from `neksus_jobspec`.
- `SECURITY.md` with private vulnerability reporting policy and supported-version guidance.
- Documentation page for security policy in `docs/project/security.md`.
- Real rendered screenshot example (`docs/assets/job-detail-soft-professional.png`) referenced by README and docs.
- Expanded user documentation with:
  - soft-professional YAML-to-UI mapping guide
  - content-vs-theme decision guide
  - render troubleshooting guide
  - `0.1.0` to `0.2.x` migration quick guide

### Changed
- BREAKING: `0.2.0` is not backward compatible with `0.1.0` JobSpec files.
- BREAKING: legacy top-level content fields (`title`, `summary`, `responsibilities`, `requirements`, etc.) are no longer accepted as the primary schema.
- JobSpecs must use the component-based page composition model (`job` + `components`).
- Rendering contract is `web | json-ld`.
- BREAKING: Removed legacy internal `neksus/` package layout.
- BREAKING: Migrated internal module paths to:
  - library: `src/neksus_jobspec/*`
  - CLI: `src/neksus_jobspec_cli/*`
- BREAKING: CLI entrypoint now resolves from `neksus_jobspec_cli.main`.
- Packaging/build config now ships only `neksus_jobspec` and `neksus_jobspec_cli`.
- BREAKING: Public Python `render_jobspec(...)` no longer writes output files directly; it returns rendered content only.
- Documentation renamed the public full example to `examples/job-detail.jobspec.yaml`.
- Documentation renamed custom CSS example file to `examples/theme-overrides.css`.

## [0.1.0] - 2026-05-03

### Added
- Initial PyPI release.
- CLI for creating, validating, and rendering JobSpec YAML.
- Markdown, HTML, and JSON rendering.
- Built-in themes.
- AGPL-3.0-or-later license.
