# Neksus JobSpec

[![CI](https://github.com/NeksusAI/NeksusJobSpec/actions/workflows/ci.yml/badge.svg)](https://github.com/NeksusAI/NeksusJobSpec/actions/workflows/ci.yml)
[![docs.jobspec.neksusai.com](https://img.shields.io/badge/docs-docs.jobspec.neksusai.com-0A66C2)](https://docs.jobspec.neksusai.com/)

Neksus JobSpec is a local-first Python package and CLI for creating structured, branded, machine-readable job campaign pages from YAML.

## Product Boundary

Included in the free/core package:
- local CLI
- local Python API
- local rendering/export/feed/sitemap
- optional local stdio MCP server
- assistant prompt packs in `skills/`

Not included:
- hosted SaaS/API
- authentication
- candidate collection/ATS workflows
- CV upload/parsing
- payments
- direct LinkedIn API posting

LinkedIn-ready JSON export is a data profile only.

## Installation

```bash
pip install neksus-jobspec
```

Optional MCP support:

```bash
pip install "neksus-jobspec[mcp]"
```

## Basic CLI Usage

```bash
neksus-jobspec --help
neksus-jobspec init
neksus-jobspec spec new backend-engineer
neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml
```

## Doctor Command

```bash
neksus-jobspec doctor
neksus-jobspec doctor --json
```

## Spec Lint and Status

```bash
neksus-jobspec spec lint examples/startup-engineer.jobspec.yaml
neksus-jobspec spec status examples/startup-engineer.jobspec.yaml
```

`spec lint` emits advisory quality warnings while schema-invalid specs still fail.

## Local Preview

```bash
neksus-jobspec spec preview examples/startup-engineer.jobspec.yaml
neksus-jobspec spec preview examples/startup-engineer.jobspec.yaml --theme classic --port 8765 --no-open
```

## Themes

```bash
neksus-jobspec themes list
neksus-jobspec themes show classic
neksus-jobspec themes init my-theme
neksus-jobspec themes validate my-theme
neksus-jobspec themes validate examples/themes/minimal
```

## Rendering and Exports

```bash
neksus-jobspec spec render examples/startup-engineer.jobspec.yaml --format web --output dist/startup-engineer.html
neksus-jobspec spec render examples/startup-engineer.jobspec.yaml --format json-ld --output dist/startup-engineer.jsonld

neksus-jobspec spec export examples/startup-engineer.jobspec.yaml --target generic-json --out dist/startup-engineer.json
neksus-jobspec spec export examples/startup-engineer.jobspec.yaml --target generic-xml --out dist/startup-engineer.xml
neksus-jobspec spec export examples/startup-engineer.jobspec.yaml --target linkedin-ready-json --out dist/startup-engineer-linkedin.json
```

## Feeds and Sitemap

```bash
neksus-jobspec feed export "examples/*.jobspec.yaml" --target jobs-json --out dist/jobs.json
neksus-jobspec feed export "examples/*.jobspec.yaml" --target jobs-xml --out dist/jobs.xml
neksus-jobspec feed sitemap "examples/*.jobspec.yaml" --base-url https://company.dk/jobs --out dist/sitemap.xml
```

## MCP Server (Optional)

```bash
neksus-jobspec-mcp
```

See docs:
- [`docs/integrations/mcp-server.md`](docs/integrations/mcp-server.md)
- [`docs/integrations/mcp-install-matrix.md`](docs/integrations/mcp-install-matrix.md)

## Documentation

- Main docs: [`docs/index.md`](docs/index.md)
- CLI reference: [`docs/reference/cli-reference.md`](docs/reference/cli-reference.md)
- Themes guide: [`docs/concepts/themes.md`](docs/concepts/themes.md)
- Exports guide: [`docs/exports.md`](docs/exports.md)
- Release notes: [`docs/project/release-notes.md`](docs/project/release-notes.md)
- Changelog: [`CHANGELOG.md`](CHANGELOG.md)

## Development Checks

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run python -m mkdocs build --strict
```

## License

AGPL-3.0-or-later. See [LICENSE](LICENSE).
