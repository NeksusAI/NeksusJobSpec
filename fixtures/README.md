# Fixtures

Small, focused YAML fixtures used by tests.

## Structure

- `valid/`
  - Contains known-good JobSpec samples.

- `invalid/`
  - Contains targeted failure cases (single-failure intent where possible).

## Current files

- `valid/backend-engineer.jobspec.yaml`
  - Baseline valid JobSpec.
- `valid/remote-software-engineer.jobspec.yaml`
  - Employer-focused remote software role.
- `valid/onsite-operations-manager.jobspec.yaml`
  - Employer-focused onsite operations role.
- `valid/hybrid-sales-executive.jobspec.yaml`
  - Employer-focused hybrid sales role with location details.

- `invalid/missing-title.jobspec.yaml`
  - Missing required `title` field.

- `invalid/empty-requirements.jobspec.yaml`
  - Empty `requirements` list (violates min length rule).

## Fixture principles

- Keep files minimal and readable.
- One primary behavior per invalid fixture.
- Prefer deterministic content for stable tests.
