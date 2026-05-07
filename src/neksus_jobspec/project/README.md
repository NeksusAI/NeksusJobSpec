# neksus_jobspec.project

Project-level configuration, discovery, initialization, and checks.

## Purpose

Encapsulates `.neksus/config.yaml` behavior and project-wide checks independent of CLI.

## Files

- `discovery.py`: project root discovery.
- `config.py`: config load/save/mutation rules.
- `init_project.py`: project scaffold creation.
- `checks.py`: project consistency checks and duplicate ID checks.

## Rule

Commands should consume this package through app-layer use cases where possible.
