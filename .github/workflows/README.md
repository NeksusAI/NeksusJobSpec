# GitHub Automation Ownership

This directory owns repository automation: CI, docs deployment, and package publishing.

## Workflows

- `.github/workflows/ci.yml`
  - Runs lint, unit tests, smoke checks, integration tests, build validation, and installed-wheel smoke.
- `.github/workflows/deploy-docs.yml`
  - Builds and deploys MkDocs site to GitHub Pages.
- `.github/workflows/publish-pypi.yml`
  - Builds and publishes tagged releases to TestPyPI then PyPI via Trusted Publishing.

## Scripts

- `.github/scripts/smoke_ci.sh`
  - CI smoke gate for repository state (CLI, fixtures, render paths, docs strict build).
- `.github/scripts/smoke_wheel.sh`
  - Post-build validation using the generated wheel in a fresh virtualenv.

## Deployment flows

### Docs deployment

1. Push to branch with docs workflow trigger enabled.
2. `deploy-docs.yml` builds with MkDocs and publishes to GitHub Pages.

### Package release deployment

1. Create and push semantic tag, e.g. `v0.2.1`.
2. `publish-pypi.yml`:
   - builds distribution,
   - uploads artifacts,
   - publishes to TestPyPI,
   - publishes to PyPI.

### CI gating

`ci.yml` enforces required quality gates before package validation and wheel smoke.
