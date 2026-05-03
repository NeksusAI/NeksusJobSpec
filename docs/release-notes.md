# Release Notes

This page tracks user-visible changes by release.

Compatibility expectations for each release are defined by the [Versioning and Compatibility Policy](versioning.md).

## 0.2.0

### Breaking changes

- None.

### Deprecations

- None.

### Notes

- Added a stable top-level public Python API surface:
  - `from neksus_jobspec import JobSpec, load_jobspec, validate_jobspec, render_jobspec`
- Added compatibility policy documentation and stable API reference docs.
- Added installed-wheel smoke validation in CI and local smoke script support.

## Release process note

When bumping a release version:

1. Update `pyproject.toml` and `neksus/__init__.py` to the same version.
2. Add or update the corresponding release notes section on this page.
