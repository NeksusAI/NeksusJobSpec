# Fixtures

Small, focused YAML fixtures used by tests.

## Structure

- `valid/`
  - Contains known-good JobSpec samples.

- `invalid/`
  - Contains targeted failure cases (single-failure intent where possible).

## Current files

- `valid/minimal-valid.jobspec.yaml`
  - Baseline valid JobSpec.

- `invalid/missing-title.jobspec.yaml`
  - Missing required `title` field.

- `invalid/empty-requirements.jobspec.yaml`
  - Empty `requirements` list (violates min length rule).

## Fixture principles

- Keep files minimal and readable.
- One primary behavior per invalid fixture.
- Prefer deterministic content for stable tests.
