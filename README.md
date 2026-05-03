# Neksus JobSpec

[![CI](https://github.com/NeksusAI/NeksusJobSpec/actions/workflows/ci.yml/badge.svg)](https://github.com/NeksusAI/NeksusJobSpec/actions/workflows/ci.yml)
[![docs.jobspec.neksusai.com](https://img.shields.io/badge/docs-docs.jobspec.neksusai.com-0A66C2)](https://docs.jobspec.neksusai.com/)
[![PyPI version](https://img.shields.io/pypi/v/neksus-jobspec)](https://pypi.org/project/neksus-jobspec/)
[![PyPI downloads](https://img.shields.io/pypi/dm/neksus-jobspec)](https://pypi.org/project/neksus-jobspec/)

Neksus JobSpec is an open-source, local-first CLI and Python package for creating, validating, and rendering structured job specifications written in YAML.

## Status

Current focus is a stable CLI and reusable core library. Hosted API and MCP server capabilities are planned, not yet implemented.

## Installation

Once published:

```bash
pip install neksus-jobspec
```

## Import example

```python
import neksus_jobspec

print(neksus_jobspec.__version__)
```

## Basic usage

```bash
neksus-jobspec init
neksus-jobspec spec new backend-engineer
neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format markdown
```

## Development

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pytest
./scripts/smoke.sh
```

## Development build commands

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine check dist/*
python -m pip install --force-reinstall dist/neksus_jobspec-0.1.0-py3-none-any.whl
python -c "import neksus_jobspec; print(neksus_jobspec.__version__)"
```

## Release process

Create and push a semantic version tag to trigger publishing:

```bash
git tag v0.1.0
git push origin v0.1.0
```

You can also run the publish workflow manually from GitHub Actions (`workflow_dispatch`).

## PyPI publishing notes

Publishing is configured through GitHub Actions Trusted Publishing (OIDC) in `.github/workflows/publish-pypi.yml`.
No PyPI API token is used by the workflow.

## License

Licensed under AGPL-3.0-or-later. See [LICENSE](LICENSE).

## Contribution policy

This repository is owner-maintained and does not use a public external contribution workflow.

## Testing Strategy

Three required layers:

- Unit/CLI layer: `uv run pytest -m "not integration"`
- Smoke layer: `./scripts/smoke.sh`
- Integration layer: `uv run pytest -m integration`

Recommended local sequence:

```bash
uv run pytest -m "not integration"
./scripts/smoke.sh
uv run pytest -m integration
```
