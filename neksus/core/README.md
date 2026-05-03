# `neksus.core`

Core domain logic for Neksus JobSpec.

This layer is reusable independently from Typer and terminal output.

## Responsibilities

- Define domain models and validation contracts.
- Parse YAML into typed models.
- Generate warnings separate from errors.
- Render JobSpecs to web and json-ld.
- Discover/configure/check projects.

## Subpackages and modules

- `jobspec/`: file-level JobSpec lifecycle (parse/validate/render/inspect/template)
- `project/`: project-level lifecycle (discovery/config/init/check)
- `errors.py`: domain exception classes
- `results.py`: stable result models shared across validators/checkers
- `output.py`: JSON helper used by CLI

## Public API strategy

`core/__init__.py` re-exports stable result types for package consumers.
