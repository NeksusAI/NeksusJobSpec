# `neksus.core.project`

Project-level behavior and invariants.

## Responsibilities

- Find project root (`.neksus/config.yaml`).
- Load/save typed project configuration.
- Initialize project skeleton.
- Execute project-wide checks across all JobSpec files.

## Modules

- `discovery.py`
  - Upward directory search for `.neksus/config.yaml`.

- `config.py`
  - `ProjectConfig` Pydantic model.
  - Mutable-key guard for `config set`.
  - Reads/writes config YAML.

- `init_project.py`
  - Creates `.neksus/config.yaml`, `jobspecs/`, `dist/`.
  - Optionally creates `jobspecs/example.jobspec.yaml`.
  - Supports overwrite via `force`.

- `checks.py`
  - Validates project directories.
  - Validates all `*.jobspec.yaml` specs.
  - Detects duplicate JobSpec IDs.
  - Applies strict warning behavior.

## Check output model

`run_project_checks(...)` returns `ProjectCheckResult` with:
- `ok`
- `checks[]`
- `errors[]`
- `warnings[]`

This structure is intentionally stable for CLI JSON consumers.
