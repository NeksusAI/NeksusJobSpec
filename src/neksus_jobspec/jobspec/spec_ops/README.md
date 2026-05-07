# neksus_jobspec.jobspec.spec_ops

Vertical operation slices for file-oriented JobSpec workflows.

## Purpose

This folder groups operations by use case rather than by technical layer.

## Files

- `new_ops.py`: list templates and create new spec files.
- `validate_ops.py`: validate YAML spec files.
- `render_ops.py`: render spec files and write schema output.
- `inspect_ops.py`: inspect metadata and campaign status payload.
- `export_ops.py`: machine-readable single-spec exports.
- `migrate_ops.py`: schema migration status.

## Rule

Each op should stay small, explicit, and focused on one user workflow.
