# Release Notes

This page tracks user-visible changes by release.

Compatibility expectations for each release are defined by the
[Versioning and Compatibility Policy](versioning.md).

## 0.4.0

### Notes

- Stability and packaging hardening for the `src/` package layout and CLI/MCP entrypoint validation.
- Added `neksus-jobspec doctor` local diagnostics command.
- Added `neksus-jobspec spec lint` quality warnings command.
- Added `neksus-jobspec spec preview` local preview server command.
- Added theme developer workflows:
  - `themes list`
  - `themes show` (built-in and filesystem/custom path support)
  - `themes validate`
  - `themes init`
- Added minimal custom theme example at `examples/themes/minimal`.
- Expanded tests for preview/lint/theme workflows and maintained deterministic machine-readable outputs.

### Scope boundary

v0.4.0 remains local-first free/core software with no hosted SaaS, ATS automation,
candidate collection, CV handling, auth, payments, or direct LinkedIn posting.

## 0.3.0

### Breaking changes

- `job.apply` moved to strict method-based metadata:
  - `email`
  - `external_url`
  - `ats_url`
  - `custom`
  - `agent_ready`
- Legacy `job.apply: {label, url}` shape is no longer accepted.

### Notes

- Added optional `campaign` metadata with validated status and date ordering.
- Added deterministic export targets for single-job output:
  - `generic-json`
  - `generic-xml`
  - `linkedin-ready-json`
- Added multi-job feed commands:
  - `jobs-json`
  - `jobs-xml`
- Added sitemap generation.
- Added optional assistant prompt packs under `skills/`.
- Added optional local stdio MCP server support via the `mcp` extra.

The MCP server is local-only and CLI/API-parity focused. It exposes local
validation, rendering, export, feed, sitemap, schema/template, theme, config,
project check, and version/init tooling. It does not collect applications,
upload CVs, send emails, process payments, manage candidates, post directly to
LinkedIn, or run hosted API infrastructure.

### Scope boundary

v0.3.0 remains the free/core package:

- local CLI
- local Python API
- local stdio MCP server
- schema validation
- rendering
- deterministic exports
- feed and sitemap generation
- assistant prompt packs

Hosted/commercial feature areas remain intentionally out of scope.

## 0.2.0

### Breaking changes

- `0.2.0` is not backward compatible with `0.1.0` JobSpec files.
- Legacy top-level content fields are removed from accepted schema.
- Internal package layout changed from `neksus/*` to:
  - `src/neksus_jobspec/*` (library)
  - `src/neksus_jobspec_cli/*` (CLI)
- CLI entrypoint now resolves from `neksus_jobspec_cli.main`.

### Deprecations

- None.

### Notes

- Stable top-level public Python API surface:
  - `from neksus_jobspec import JobSpec, load_jobspec, validate_jobspec, render_jobspec`
- Compatibility policy and API reference docs updated.
- Installed-wheel smoke validation is owned under `.github/scripts/smoke_wheel.sh`.

## Release process note

When bumping a release version:

1. Update `pyproject.toml` and `src/neksus_jobspec/__init__.py` to the same version.
2. Add or update the corresponding release notes section on this page.
3. Use `neksus-jobspec spec render ... --output <path>` (not `--out`) for render docs/examples.
