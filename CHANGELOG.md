# Changelog

All notable user-visible changes to this project are documented in this file.

The format is inspired by Keep a Changelog and follows Semantic Versioning.

## [Unreleased]

### Added
- Controlled composable job-detail page components (`components`) with typed validation.
- Page/component-based rendering support across web and json-ld.
- Danish/Nordic job-detail example at `examples/danish-job-detail.jobspec.yaml`.
- New Stitch-aligned built-in `soft-professional` web theme as the only supported theme.
- New theme guide: `docs/themes.md` (built-ins, overrides, and custom-template directory usage).
- New structural components: `header_brand`, `hero_banner`, `meta_panel`, `social_links`, `location_map`, and `footer_brand`.
- New composition components: `nav_links`, `header_actions`, `feature_grid`, and `meta_chips`.
- Placement-aware composition fields on all components: `placement` and `container`.
- Configurable web asset URL prefixing via `rendering.web.asset_base_url` and CLI `--asset-base-url`.
- Configurable top apply CTA visibility via `rendering.web.show_top_apply`.
- Configurable localized web labels via `rendering.web.labels` (`share`, `print`, `phone`, `mobile`, `email`, `open_map`, `deadline`).
- Pinned Stitch contract fixtures for `soft-professional` parity:
  - `fixtures/stitch/isolated-jobspec-output.soft-professional.html`
  - `fixtures/stitch/isolated-jobspec-output.soft-professional.png`

### Changed
- JobSpec model is now component-first (`page`, `job`, `components`, `rendering`) and removes legacy v0.1.0 content compatibility.
- Documentation expanded for assistant usage, compatibility policy, specification, rendering, and examples.
- `spec render --no-validate` now explicitly describes warning-check behavior.
- BREAKING: legacy/simple schema compatibility paths were removed in `0.2.x`; validation now explicitly reports migration guidance.
- BREAKING: rendering contract is now `web | json-ld` only; removed render formats are rejected with migration guidance.
- BREAKING: when `page.component_order` is provided, it must include every component ID exactly once.
- BREAKING: multi-theme support was removed; `soft-professional` is the only built-in theme in v0.2.x.
- Web renderer now emits explicit layout regions (`jobspec-fullwidth`, `jobspec-main`, `jobspec-sidebar`) and respects per-component `placement`.
- Facts and meta panel entries now support optional `icon`.
- Benefits and social links now support optional icon-bearing entries for richer web composition.
- Danish demo example content is anonymized (company, contacts, location, and visual asset) for safe redistribution/deployment.
- `soft-professional` web rendering now emits the canonical Stitch reference output for deterministic byte-level parity across CLI entry points.

### Fixed
- Release hygiene updates across docs and agent guidance.
- Removed dead/unused rendering code and no-op settings from the active v0.2.x surface:
  - removed unused markdown renderer module
  - removed unused `custom_template_dir` wiring and CLI flags
  - removed automatic JavaScript sidecar file emission during web render output
  - simplified normalized render model to avoid redundant placement lists
- Security hardening for rendered HTML:
  - blocks unsafe URL schemes in component URLs
  - blocks unsafe component attribute keys (including event-handler attributes)
- Web renderer now preserves fullwidth component flow (top fullwidth region vs trailing fullwidth region), fixing misplaced fullwidth footer composition.

## [0.2.0]

### Changed
- BREAKING: `0.2.0` is not backward compatible with `0.1.0` JobSpec files.
- BREAKING: legacy top-level content fields (`title`, `summary`, `responsibilities`, `requirements`, etc.) are no longer accepted as the primary schema.
- JobSpecs must use the v0.2.0 component-based page composition model (`job` + `components`).

### Added
- Public Python API from `neksus_jobspec`.
- LLM/assistant guidance documentation and `llms.txt`.
- Versioning and compatibility policy documentation.
- Installed-wheel smoke validation in CI and `scripts/smoke_wheel.sh`.
- Controlled composable job-detail page components.
- Page/component-based rendering support.
- Danish/Nordic job-detail example.

## [0.1.0] - 2026-05-03

### Added
- Initial PyPI release.
- CLI for creating, validating, and rendering JobSpec YAML.
- Markdown, HTML, and JSON rendering.
- Built-in themes.
- AGPL-3.0-or-later license.
