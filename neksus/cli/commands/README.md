# `neksus.cli.commands`

Each file here contains one command group or shared command helper.

## Modules

- `common.py`
  - Shared `stdout`/`stderr` consoles.
  - JSON serialization helper.
  - Central exception-to-exit-code mapping.

- `version.py`
  - Implements `neksus-jobspec version`.
  - Returns package/version info in human or JSON format.

- `init.py`
  - Implements `neksus-jobspec init`.
  - Delegates to project init core logic.

- `spec.py`
  - Implements `spec` subgroup:
    - `new`
    - `validate`
    - `render`
    - `templates`
    - `schema`
    - `inspect`
    - `migrate`
  - Handles strict mode and output mode branching.

- `render.py`
  - Implements top-level `neksus-jobspec render`.
  - Renders all project JobSpecs to configured output directory.

- `check.py`
  - Implements `neksus-jobspec check`.
  - Delegates project-wide validation and duplicates scan.

- `config.py`
  - Implements `config get` and `config set`.
  - Uses project discovery + config validation from core.

## Exit code contract

- `0`: success
- `1`: validation/project-check failure
- `2`: CLI usage error
- `3`: filesystem error
- `4`: config error
- `5`: internal/unknown error
