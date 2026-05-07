# Changelog

All notable user-visible changes to this project are documented in this file.

The format is inspired by Keep a Changelog and follows Semantic Versioning.

## [Unreleased]

### Added

- No entries yet.

### Changed

- No entries yet.

## [0.3.0]

### Added

- Optional `campaign` metadata (`starts_at`, `expires_at`, `status`) with schema validation.
- New apply destination metadata with method-based contract:
  - `email`
  - `external_url`
  - `ats_url`
  - `custom`
  - `agent_ready`
- Single-job exports via `neksus-jobspec spec export`:
  - `generic-json`
  - `generic-xml`
  - `linkedin-ready-json`
- Multi-job feeds via `neksus-jobspec feed export`:
  - `jobs-json`
  - `jobs-xml`
- Sitemap generation via `neksus-jobspec feed sitemap`.
- Optional assistant prompt packs in `skills/` for ChatGPT, Claude, Copilot, and Gemini.
- Optional local stdio MCP server support via the `mcp` extra:
  - executable: `neksus-jobspec-mcp`
  - local CLI/API-parity tools for project/config/check, spec schema/template/new/validate/render/inspect/status/migrate/export, feed export, and sitemap generation.
- MCP integration documentation and assistant install matrix for Claude, ChatGPT, Gemini, and Copilot.
- Added two built-in web themes: `classic` and `classic-dark`.
- Added prototype-aligned web rendering variants for `classic` and `classic-dark` with graceful omission of missing optional sections.
- Added Jinja2-based theme package rendering infrastructure.
- Added filesystem custom theme package support (`manifest.json` + Jinja template + CSS assets).

### Changed

- BREAKING: `job.apply` no longer accepts legacy `{label, url}` shape.
- JSON-LD `validThrough` now maps from `campaign.expires_at` when provided.
- Web rendering shows a visible closed/expired campaign notice.
- Release and assistant docs were reformatted for readability and v0.3.0 scope clarity.
- Version bumped to `0.3.0`.
- Introduced a shared `ThemeRenderContext` contract and unified built-in/custom web rendering pipeline through package validation + Jinja rendering.
- Added centralized theme package compatibility validation (`validate_theme_package`) for manifest structure, mandatory component support, region support, and context compatibility.
- Rendering config now uses `rendering.web.theme_config` as the canonical per-theme configuration surface for web presentation settings.
- Removed CLI/MCP/Python runtime CSS override paths (`--css` / `--no-css` and related API fields). Web styling now comes only from built-in or custom theme packages.
- Removed compatibility fallback branch selection from HTML rendering; web rendering now uses only the unified theme-package contract path.
- Built-in and custom theme templates now consume the shared `contract` context directly, and rendering parity matrix tests were added for built-in/custom paths.
- Removed theme-specific adapter dataclasses/mappers from `html.py`; templates now read canonical component payloads from `contract.component_groups`.
- Rendering contracts were reorganized by output target through typed Pydantic target models (`rendering/targets.py`) for JSON-LD, jobs feeds, and sitemap output generation.
- Feed and sitemap generation now run through typed render-target models before JSON/XML serialization, replacing ad-hoc dict/XML assembly in the old `jobspec/feeds.py` module.
- JSON-LD rendering now builds a typed `JsonLdJobPosting` model before serialization, replacing ad-hoc payload assembly in the old `rendering/json_ld.py` module.
- Built-in theme templates now source section labels, campaign notices, map label prefix, and footer/legal links from YAML/config contracts instead of hardcoded text.
- Restored visual parity defaults in built-in theme assets (including `soft-professional` tokenized Tailwind config and classic/classic-dark footer-link defaults) while keeping rendering template-driven.
- `meta_chips` items now support an optional `semantic` key (`location`, `salary`, `employment`) to avoid fragile label-text inference in theme rendering.
- Web renderer now dispatches through theme package resolution and Jinja templates.
- Theme/config validation now accepts `classic`, `classic-dark`, and `custom` for project defaults and render profiles.
- Custom theme validation now enforces known component/region contracts and required package files.
- Documentation now includes dedicated user guides and one screenshot per built-in theme (`soft-professional`, `classic`, `classic-dark`).
- Internal orchestration for `spec new`, `spec validate`, `spec render`, `spec inspect`, `spec status`, `spec export`, `spec schema`, `spec templates`, `spec migrate`, project `check` and `config get/set`, and feed `export`/`sitemap` is now shared through a core application use-case layer used by both CLI and local MCP handlers.
- JobSpec operation modules are reorganized into vertical slices under `neksus_jobspec.jobspec.spec_ops`, and project use cases now share a `ProjectContext` for root/config resolution.
- App-layer use cases now return typed DTO payloads for core spec/project flows, and input-contract errors are normalized through domain exceptions.
- Added domain methods on `JobSpec` for campaign status, theme resolution, warning derivation, and export payload shaping, and wired validation/status/export paths to use these model-level contracts.
- Batch `render` orchestration moved from CLI command code into `RenderUseCase` with shared filesystem gateway handling.
- Tests are now organized by layer (`tests/cli`, `tests/core`, `tests/mcp`, `tests/arch`, `tests/integration`) with architecture boundary checks for CLI/app/MCP layering.
- MkDocs strict-build docs fixes: added `reference/code-structure.md` to navigation and removed invalid links to non-doc `src/...` paths from reference pages.

### Security

- Explicit product boundary in release docs:
  - no application collection
  - no `application_form` schema
  - no CV upload/parsing
  - no candidate storage
  - no email delivery
  - no payments
  - no hosted API/frontend/infrastructure
  - no ATS workflow automation
  - no direct LinkedIn posting integration

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
- BREAKING: removed legacy internal `neksus/` package layout.
- BREAKING: migrated internal module paths to:
  - library: `src/neksus_jobspec/*`
  - CLI: `src/neksus_jobspec_cli/*`
- BREAKING: CLI entrypoint now resolves from `neksus_jobspec_cli.main`.
- Packaging/build config now ships only `neksus_jobspec` and `neksus_jobspec_cli`.
- BREAKING: public Python `render_jobspec(...)` no longer writes output files directly; it returns rendered content only.
- Documentation renamed the public full example to `examples/job-detail.jobspec.yaml`.
- Documentation renamed custom CSS example file to `examples/theme-overrides.css`.

## [0.1.0] - 2026-05-03

### Added

- Initial PyPI release.
- CLI for creating, validating, and rendering JobSpec YAML.
- Markdown, HTML, and JSON rendering.
- Built-in themes.
- AGPL-3.0-or-later license.
