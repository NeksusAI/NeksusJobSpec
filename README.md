# Neksus JobSpec

Employer-side JobSpec builder for teams that want **version-controlled hiring specs** with **strict validation** and **clean outputs**.

Write a JobSpec in YAML, then run:

```bash
neksus-jobspec render --format markdown
neksus-jobspec render --format html --theme modern
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format html --theme modern --css examples/jobspec.css
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format html --no-css
```

and get deterministic, human-readable output.

## Why Neksus JobSpec?

With Neksus JobSpec, you can:

- Version-control hiring specs because they are plain text.
- Separate content from formatting.
- Validate specs with explicit, stable errors and warnings.
- Export JSON Schema for editor autocomplete and tooling.

## Get Started

### 1. Install

```bash
pip install neksus-jobspec
```

For local development:

```bash
uv sync
```

### 2. Initialize a project

```bash
neksus-jobspec init
```

This creates:

- `.neksus/config.yaml`
- `jobspecs/`
- `dist/`
- `jobspecs/example.jobspec.yaml` (unless `--empty`)

### 3. Create and validate a spec

```bash
neksus-jobspec spec new backend-engineer
neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml
```

### 4. Render outputs

```bash
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format markdown --output dist/backend-engineer.md
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format html --output dist/backend-engineer.html
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format json --output dist/backend-engineer.json
neksus-jobspec render --format markdown
neksus-jobspec render --format html --theme modern
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format html --theme modern --css examples/jobspec.css
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format html --no-css
```

### 5. Export schema for editor support

```bash
neksus-jobspec spec schema --output schemas/jobspec.v1.json
neksus-jobspec spec schema --json
```

## CLI Commands

- `neksus-jobspec version`
- `neksus-jobspec init`
- `neksus-jobspec spec new NAME`
- `neksus-jobspec spec validate PATH`
- `neksus-jobspec spec render PATH`
- `neksus-jobspec spec templates`
- `neksus-jobspec spec schema`
- `neksus-jobspec spec inspect PATH`
- `neksus-jobspec spec migrate PATH`
- `neksus-jobspec render`
- `neksus-jobspec check`
- `neksus-jobspec themes`
- `neksus-jobspec themes show NAME`
- `neksus-jobspec config get [KEY]`
- `neksus-jobspec config set KEY VALUE`

## Strict Validation

Validation separates:

- **Errors**: fail validation.
- **Warnings**: advisory by default.

Use strict mode to fail on warnings:

```bash
neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml --strict
neksus-jobspec check --strict
```

## Documentation

- [User Guide](docs/user_guide/get-started.md)
- [CLI Reference](docs/user_guide/cli-reference.md)
- [JobSpec Structure](docs/user_guide/jobspec-structure.md)
- [Developer Setup](docs/developer_guide/setup.md)
- [Release Process](docs/releasing.md)
- [Documentation Index](docs/README.md)

## Development

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

## Packaging

```bash
python -m pip install build twine
python -m build
twine check dist/*
```
