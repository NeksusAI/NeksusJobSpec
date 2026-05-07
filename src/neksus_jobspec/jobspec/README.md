# neksus_jobspec.jobspec

JobSpec domain logic and rendering/validation primitives.

## Purpose

This folder contains the canonical schema model and all transformation logic from YAML input to rendered/exported outputs.

## Structure

- `models.py`: Pydantic models and model-level domain helpers.
- `parser.py`: YAML loading and parse/validation mapping.
- `validator.py`: normalized validation/warning result shaping.
- `renderer.py`: format-level render wrapper (`web`, `json-ld`).
- `rendering/`: target-oriented rendering backends and theme engine implementations.
- `exports.py`: deterministic machine-readable single-job exports.
- `inspect.py`: metadata extraction for inspect flows.
- `schema.py`: JSON Schema generation.
- `templates.py`: template scaffold generation.
- `migrate.py`: schema migration status inspection.
- `spec_ops/`: vertical operation slices used by app-layer use cases.

## Public stability note

Public CLI behavior is stable by contract. Internal Python module APIs in this folder may evolve.
