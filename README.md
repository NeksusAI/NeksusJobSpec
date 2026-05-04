# Neksus JobSpec

[![CI](https://github.com/NeksusAI/NeksusJobSpec/actions/workflows/ci.yml/badge.svg)](https://github.com/NeksusAI/NeksusJobSpec/actions/workflows/ci.yml)
[![docs.jobspec.neksusai.com](https://img.shields.io/badge/docs-docs.jobspec.neksusai.com-0A66C2)](https://docs.jobspec.neksusai.com/)
[![PyPI version](https://img.shields.io/pypi/v/neksus-jobspec)](https://pypi.org/project/neksus-jobspec/)
[![PyPI downloads](https://img.shields.io/pypi/dm/neksus-jobspec)](https://pypi.org/project/neksus-jobspec/)

Neksus JobSpec is an open-source, local-first CLI and Python package for creating, validating, and rendering structured job specifications written in YAML.

## Status

Current focus is a stable CLI and reusable core library. Hosted API and MCP server capabilities are planned, not yet implemented.

## Job page composition

v0.2.x uses controlled, Lego-brick-like job-detail page components.
You can compose validated page blocks such as header_brand, hero_banner, hero, meta_panel, CTA, responsibilities, requirements, benefits, quote, social_links, location_map, company profile, and legal blocks without defaulting to arbitrary HTML.

`soft-professional` is rendered from YAML components plus the built-in theme.

- Example: [`examples/job-detail.jobspec.yaml`](examples/job-detail.jobspec.yaml)
- Docs: [`docs/specification.md`](docs/specification.md), [`docs/rendering.md`](docs/rendering.md), [`docs/themes.md`](docs/themes.md), [`docs/examples.md`](docs/examples.md)
- Deep dives: [`docs/soft-professional-guide.md`](docs/soft-professional-guide.md), [`docs/content-vs-theme.md`](docs/content-vs-theme.md), [`docs/render-troubleshooting.md`](docs/render-troubleshooting.md), [`docs/migration-0.1-to-0.2.md`](docs/migration-0.1-to-0.2.md)

Rendered example screenshot:

![Soft Professional Job Detail](docs/assets/job-detail-soft-professional.png)

For portable web output paths, use `rendering.web.asset_base_url` in spec files or `--asset-base-url` in CLI rendering commands.

## Installation

```bash
pip install neksus-jobspec
```

## Quickstart

```bash
pip install neksus-jobspec
mkdir neksus-jobspec-demo
cd neksus-jobspec-demo
neksus-jobspec init
neksus-jobspec spec new backend-engineer
neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format web --output dist/backend-engineer.html
```

## Python API

```python
from neksus_jobspec import JobSpec, load_jobspec, render_jobspec, validate_jobspec

spec = load_jobspec("jobspecs/backend-engineer.jobspec.yaml")
validated = validate_jobspec(spec.model_dump())
web = render_jobspec(validated, format="web")
print(web[:80])
```

## Basic CLI usage

```bash
neksus-jobspec init
neksus-jobspec spec new backend-engineer
neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format web
neksus-jobspec themes
neksus-jobspec themes show soft-professional
```

## Development

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run pytest -m integration && uv run python -m mkdocs build --strict
```

## Development build commands

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine check dist/*
python -m pip install --force-reinstall dist/neksus_jobspec-*.whl
python -c "import neksus_jobspec; print(neksus_jobspec.__version__)"
```

## Release process

Create and push a semantic version tag to trigger publishing:

```bash
git tag v0.2.0
git push origin v0.2.0
```

You can also run the publish workflow manually from GitHub Actions (`workflow_dispatch`).

Release notes are maintained in [`docs/release-notes.md`](docs/release-notes.md), with compatibility expectations defined in [`docs/versioning.md`](docs/versioning.md).
See full change history in [`CHANGELOG.md`](CHANGELOG.md).
Security reporting and support policy: [`SECURITY.md`](SECURITY.md).

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
- Smoke layer: `uv run pytest -m integration && uv run python -m mkdocs build --strict`
- Integration layer: `uv run pytest -m integration`

Recommended local sequence:

```bash
uv run pytest -m "not integration"
uv run pytest -m integration && uv run python -m mkdocs build --strict
uv run pytest -m integration
```
