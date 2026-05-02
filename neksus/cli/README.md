# `neksus.cli`

This package implements the command-line interface using Typer.

## Responsibilities

- Define command tree and subcommands.
- Parse CLI args/options into typed Python values.
- Call `neksus.core` functions.
- Format output (human or JSON).
- Map known errors to stable exit codes.

## Files

- `main.py`: root Typer app and command registration.
- `commands/`: command implementations by domain area.

## Command tree

Root command: `neksus-jobspec`

- `version`
- `init`
- `spec ...`
- `check`
- `config ...`

## Error handling model

All command handlers follow the same pattern:
1. Execute core logic in a `try` block.
2. On known exceptions, call `handle_expected_error(...)`.
3. Return machine-readable JSON when `--json` is enabled.
4. Raise `typer.Exit(code)` where explicit non-zero exit is needed.
