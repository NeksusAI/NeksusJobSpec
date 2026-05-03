# Internal API Reference

This page is for power users exploring internals programmatically.

## Stability disclaimer

Internal Python APIs are **not guaranteed stable** and may change without notice between releases.
See [Versioning and Compatibility Policy](versioning.md) for the supported compatibility contract.

## CLI entrypoints

- `neksus.cli.main`
  - Registers top-level Typer commands and command groups.
- `neksus.cli.commands.*`
  - Thin wrappers over core logic.

## Core JobSpec modules

- `neksus.core.jobspec.models`
  - Canonical Pydantic models (`JobSpec`, `Location`, `Employment`).
- `neksus.core.jobspec.parser`
  - YAML reading and conversion to validated models.
- `neksus.core.jobspec.validator`
  - Normalizes validation issues and warning collection.
- `neksus.core.jobspec.renderer`
  - Compatibility wrapper over render options/backends.
- `neksus.core.jobspec.inspect`
  - Inspection metadata for CLI inspect output.
- `neksus.core.jobspec.schema`
  - JSON Schema generation from live model.

## Core project modules

- `neksus.core.project.config`
  - Project config model, loading, and mutation helpers.
- `neksus.core.project.discovery`
  - Project-root discovery.
- `neksus.core.project.checks`
  - Project-wide validity checks and duplicate-id detection.

## Result and error contracts

- `neksus.core.results`
  - `ValidationIssue`, `ValidationResult`, `ProjectCheck`, `ProjectCheckResult`.
- `neksus.core.errors`
  - Domain exceptions (`ConfigError`, `FileSystemError`, `JobSpecParseError`, etc.).

## Suggested integration stance

- Prefer CLI invocation for stable automation behavior.
- If importing Python internals, pin versions and expect refactors.
