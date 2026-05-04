# Changelog

All notable user-visible changes to this project are documented in this file.

The format is inspired by Keep a Changelog and follows Semantic Versioning.

## [0.2.0]

### Added
- Controlled composable job-detail page components.
- Structured validation and project checks for component-based specs.
- Built-in `soft-professional` web theme.
- Public Python API from `neksus_jobspec`.
- `SECURITY.md` with private vulnerability reporting policy and supported-version guidance.
- Documentation page for security policy in `docs/security.md`.
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
- Documentation renamed the public full example to `examples/job-detail.jobspec.yaml`.
- Documentation renamed custom CSS example file to `examples/theme-overrides.css`.

## [0.1.0] - 2026-05-03

### Added
- Initial PyPI release.
- CLI for creating, validating, and rendering JobSpec YAML.
- Markdown, HTML, and JSON rendering.
- Built-in themes.
- AGPL-3.0-or-later license.
