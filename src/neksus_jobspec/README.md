# neksus_jobspec

Core Python package for Neksus JobSpec.

## Purpose

This package contains reusable domain logic used by:

- the CLI package (`neksus_jobspec_cli`)
- the local MCP package (`neksus_jobspec_mcp`)
- direct Python imports

## Submodules

- [`app/`](./app/README.md): application use cases, DTOs, and orchestration boundaries.
- [`jobspec/`](./jobspec/README.md): JobSpec domain model, parsing, validation, rendering, exports.
- [`project/`](./project/README.md): project discovery, config handling, and project checks.
- `errors.py`: stable domain exception types.
- `results.py`: structured validation/project result contracts.
- `output.py`: JSON output helper.

## Boundary rule

This package must remain independent from Typer command modules.
