# Neksus JobSpec

Neksus JobSpec is a local-first CLI and Python package for creating, validating, inspecting, and rendering structured JobSpec YAML files.

## Install (local)

```bash
pip install -e .
```

## Quick start

```bash
neksus-jobspec init
neksus-jobspec spec new backend-engineer
neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --output dist/backend-engineer.md
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format html --output dist/backend-engineer.html
neksus-jobspec spec schema --output schemas/jobspec.v1.json
neksus-jobspec check
```

## Commands

- `neksus-jobspec version`
- `neksus-jobspec init`
- `neksus-jobspec spec new NAME`
- `neksus-jobspec spec validate PATH`
- `neksus-jobspec spec render PATH`
- `neksus-jobspec spec schema`
- `neksus-jobspec spec inspect PATH`
- `neksus-jobspec check`
- `neksus-jobspec config get [KEY]`
- `neksus-jobspec config set KEY VALUE`

## Example JobSpec

```yaml
schema_version: 1
id: backend-engineer
title: Backend Engineer
summary: "Describe the role."
responsibilities:
  - "Define the main responsibilities."
requirements:
  - "Define the core requirements."
nice_to_have: []
```

## Development

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

## Packaging

Build distribution artifacts:

```bash
python -m pip install build
python -m build
```

This creates:
- `dist/*.tar.gz` (source distribution)
- `dist/*.whl` (wheel)

For the full release process, see `docs/releasing.md`.

## Documentation

See [docs/README.md](docs/README.md) for user guides and module docs.
