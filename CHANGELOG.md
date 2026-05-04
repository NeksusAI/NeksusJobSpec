# Changelog

All notable user-visible changes to this project are documented in this file.

The format is inspired by Keep a Changelog and follows Semantic Versioning.

## [Unreleased]

## [0.2.0]

### Changed
- BREAKING: `0.2.0` is not backward compatible with `0.1.0` JobSpec files.
- BREAKING: legacy top-level content fields (`title`, `summary`, `responsibilities`, `requirements`, etc.) are no longer accepted as the primary schema.
- JobSpecs must use the component-based page composition model (`job` + `components`).
- Rendering contract is `web | json-ld`.

### Added
- Controlled composable job-detail page components.
- Structured validation and project checks for component-based specs.
- Built-in `soft-professional` web theme.
- Public Python API from `neksus_jobspec`.
- Documentation set for schema, rendering, themes, versioning, and examples.

## [0.1.0] - 2026-05-03

### Added
- Initial PyPI release.
- CLI for creating, validating, and rendering JobSpec YAML.
- Markdown, HTML, and JSON rendering.
- Built-in themes.
- AGPL-3.0-or-later license.
