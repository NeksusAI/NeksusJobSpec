# Test Suite

Pytest suite for CLI and core behaviors.

## Goals

- Validate command behavior and exit codes.
- Validate stable JSON shapes.
- Validate model constraints and project checks.
- Keep tests filesystem-isolated (no dependency on user machine state).

## Layout

- `tests/cli/`
  - CLI command behavior, JSON shape, and exit-code contracts.

- `tests/core/`
  - core domain models, renderer/theme behavior, project checks/config, and public API.

- `tests/mcp/`
  - local MCP service parity tests.

- `tests/arch/`
  - architecture boundary checks (`cli -> app -> core`).

- `tests/integration/`
  - real end-to-end flows and local MCP integration.

## Testing style

- Typer `CliRunner` for CLI-level tests.
- Temporary/isolated filesystem contexts.
- Explicit assertions on exit code + meaningful output.


## Test layers

- Unit/CLI tests: `pytest -m "not integration"`
- Integration tests: `pytest -m integration` (real CLI + filesystem)
- Smoke tests: `uv run pytest -m integration && uv run python -m mkdocs build --strict` (fast end-to-end gate)
