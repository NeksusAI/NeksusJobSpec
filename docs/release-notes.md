# Release Notes

This page tracks user-visible changes by release.

Compatibility expectations for each release are defined by the [Versioning and Compatibility Policy](versioning.md).

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
