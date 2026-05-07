# Internal API Reference

This page is for power users exploring internals programmatically.

## Stability disclaimer

Internal Python APIs are **not guaranteed stable** and may change without notice between releases.
See [Versioning and Compatibility Policy](../project/versioning.md) for the supported compatibility contract.

## CLI entrypoints

- `neksus_jobspec_cli.main`
  - Registers top-level Typer commands and command groups.
- `neksus_jobspec_cli.commands.*`
  - Thin wrappers over core logic.

## Core JobSpec modules

- `neksus_jobspec.jobspec.models`
  - Canonical Pydantic models (`JobSpec`, `Location`, `Employment`).
- `neksus_jobspec.jobspec.parser`
  - YAML reading and conversion to validated models.
- `neksus_jobspec.jobspec.validator`
  - Normalizes validation issues and warning collection.
- `neksus_jobspec.jobspec.renderer`
  - Compatibility wrapper over render options/backends.
- `neksus_jobspec.jobspec.inspect`
  - Inspection metadata for CLI inspect output.
- `neksus_jobspec.jobspec.schema`
  - JSON Schema generation from live model.

## Core project modules

- `neksus_jobspec.project.config`
  - Project config model, loading, and mutation helpers.
- `neksus_jobspec.project.discovery`
  - Project-root discovery.
- `neksus_jobspec.project.checks`
  - Project-wide validity checks and duplicate-id detection.

## Result and error contracts

- `neksus_jobspec.results`
  - `ValidationIssue`, `ValidationResult`, `ProjectCheck`, `ProjectCheckResult`.
- `neksus_jobspec.errors`
  - Domain exceptions (`ConfigError`, `FileSystemError`, `JobSpecParseError`, etc.).

## Suggested integration stance

- Prefer CLI invocation for stable automation behavior.
- If importing Python internals, pin versions and expect refactors.

## Internal codebase docs map

- Core package overview: `src/neksus_jobspec/README.md`
- App layer: `src/neksus_jobspec/app/README.md`
- JobSpec domain: `src/neksus_jobspec/jobspec/README.md`
- JobSpec vertical ops: `src/neksus_jobspec/jobspec/spec_ops/README.md`
- Rendering internals: `src/neksus_jobspec/jobspec/rendering/README.md`
- Project internals: `src/neksus_jobspec/project/README.md`
- CLI package: `src/neksus_jobspec_cli/README.md`
- CLI commands: `src/neksus_jobspec_cli/commands/README.md`
- MCP package: `src/neksus_jobspec_mcp/README.md`
