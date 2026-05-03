# Test Suite

Pytest suite for CLI and core behaviors.

## Goals

- Validate command behavior and exit codes.
- Validate stable JSON shapes.
- Validate model constraints and project checks.
- Keep tests filesystem-isolated (no dependency on user machine state).

## Files

- `test_cli_init.py`
  - `init`, `init --empty`, overwrite refusal behavior.

- `test_cli_spec_validate.py`
  - valid/invalid validation paths and JSON payload shape.

- `test_cli_spec_render.py`
  - render-to-stdout, render-to-file, inspect JSON.

- `test_cli_spec_new_and_config.py`
  - spec scaffolding and config key validation.

- `test_project_checks.py`
  - project check pass path and duplicate-id failure.

- `test_jobspec_models.py`
  - schema-level constraints in Pydantic models.

## Testing style

- Typer `CliRunner` for CLI-level tests.
- Temporary/isolated filesystem contexts.
- Explicit assertions on exit code + meaningful output.


## Test layers

- Unit/CLI tests: `pytest -m "not integration"`
- Integration tests: `pytest -m integration` (real CLI + filesystem)
- Smoke tests: `./scripts/smoke.sh` (fast end-to-end gate)
