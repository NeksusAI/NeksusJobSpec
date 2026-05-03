# Model Reference

This page documents the current `JobSpec` model contract (`schema_version: 1`).

## Top-level model: `JobSpec`

- `schema_version: int = 1`
  - Constraint: must be exactly `1`.
- `id: str`
  - Constraint: slug pattern `^[a-z0-9]+(?:-[a-z0-9]+)*$`.
- `title: str`
  - Constraint: non-empty after trim.
- `department: str | None`
- `level: str | None`
- `location: Location | None`
- `summary: str`
  - Constraint: non-empty after trim.
- `responsibilities: list[str]`
  - Constraint: at least one item; each item non-empty after trim.
- `requirements: list[str]`
  - Constraint: at least one item; each item non-empty after trim.
- `nice_to_have: list[str]`
  - Default: empty list; each item non-empty after trim.
- `employment: Employment | None`

## Nested model: `Location`

- `type: "remote" | "hybrid" | "onsite"`
- `city: str | None`
- `country: str | None`

## Nested model: `Employment`

- `type: "full-time" | "part-time" | "contract" | "internship"`

## Warning-level rules

Warnings are generated separately from hard validation errors:

- very short title
- duplicate responsibilities (case-insensitive normalized comparison)
- duplicate requirements (case-insensitive normalized comparison)
- hybrid/onsite role missing both city and country

## Strict mode behavior

- `spec validate --strict` and `check --strict` treat warnings as failures.
- Project config `strict_validation: true` also enforces warning failures during project checks.

## Versioning and migration expectations

- Only `schema_version: 1` is accepted now.
- Use `spec migrate PATH` to inspect schema-version status.
- `--write` migration mode is currently reserved and not implemented.
