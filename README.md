# Neksus JobSpec

[![CI](https://github.com/NeksusAI/NeksusJobSpec/actions/workflows/ci.yml/badge.svg)](https://github.com/NeksusAI/NeksusJobSpec/actions/workflows/ci.yml)
[![docs.jobspec.neksusai.com](https://img.shields.io/badge/docs-docs.jobspec.neksusai.com-0A66C2)](https://docs.jobspec.neksusai.com/)
[![PyPI version](https://img.shields.io/pypi/v/neksus-jobspec)](https://pypi.org/project/neksus-jobspec/)
[![PyPI downloads](https://img.shields.io/pypi/dm/neksus-jobspec)](https://pypi.org/project/neksus-jobspec/)

## What is NeksusJobSpec?

NeksusJobSpec is an open, local-first CLI and Python package for structured,
branded, machine-readable job campaigns.

## What it does

- Defines JobSpec files in YAML.
- Validates specs against the v0.3.x schema.
- Renders output for web and JSON-LD.
- Exports deterministic single-job and multi-job machine-readable artifacts.
- Generates job sitemaps.
- Provides an optional local stdio MCP server for CLI/API-parity tooling.
- Provides optional assistant skill/prompt packs in `skills/`.

## What it does not do

It does not collect applications, upload CVs, send emails, take payments,
manage candidates, or post directly to LinkedIn.

It does not provide a hosted API, hosted frontend, ATS workflow automation,
or cloud infrastructure features.

## Installation

```bash
pip install neksus-jobspec
```

Optional MCP extra:

```bash
pip install "neksus-jobspec[mcp]"
```

## Quick start

```bash
mkdir neksus-jobspec-demo
cd neksus-jobspec-demo
neksus-jobspec init
neksus-jobspec spec new backend-engineer
```

## Validate a JobSpec

```bash
neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml
```

## Render web output

```bash
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml \
  --format web \
  --output dist/backend-engineer.html
```

Available built-in `web` themes: `classic`, `classic-dark`, `soft-professional`.

Use a custom theme package directory:

```bash
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml \
  --format web \
  --theme ./my-theme-package \
  --output dist/backend-engineer-custom.html
```

## Render JSON-LD

```bash
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml \
  --format json-ld \
  --output dist/backend-engineer.jsonld
```

## Export generic JSON/XML

```bash
neksus-jobspec spec export jobspecs/backend-engineer.jobspec.yaml \
  --target generic-json \
  --out dist/backend-engineer.json

neksus-jobspec spec export jobspecs/backend-engineer.jobspec.yaml \
  --target generic-xml \
  --out dist/backend-engineer.xml
```

## Export LinkedIn-ready JSON

```bash
neksus-jobspec spec export jobspecs/backend-engineer.jobspec.yaml \
  --target linkedin-ready-json \
  --out dist/backend-engineer-linkedin.json
```

This is a data export profile. It is not a LinkedIn API posting integration.

## Export multi-job feeds

```bash
neksus-jobspec feed export "examples/*.jobspec.yaml" \
  --target jobs-json \
  --out dist/jobs.json

neksus-jobspec feed export "examples/*.jobspec.yaml" \
  --target jobs-xml \
  --out dist/jobs.xml
```

## Generate sitemap

```bash
neksus-jobspec feed sitemap "examples/*.jobspec.yaml" \
  --base-url https://company.dk/jobs \
  --out dist/sitemap.xml
```

## Optional MCP server

The local MCP server is optional and local-only.

```bash
neksus-jobspec-mcp
```

- Install via the `mcp` extra.
- Uses stdio transport for local MCP clients.
- Exposes local CLI/API-parity tools only.
- It is not a hosted API, ATS integration, or direct LinkedIn posting tool.

See:

- [`docs/integrations/mcp-server.md`](docs/integrations/mcp-server.md)
- [`docs/integrations/mcp-install-matrix.md`](docs/integrations/mcp-install-matrix.md)

## Assistant skill/prompt packs

Assistant prompt packs are available in [`skills/`](skills/):

- ChatGPT
- Claude
- Copilot
- Gemini

## Project boundary

NeksusJobSpec v0.3.0 is the free/open-source core package.

Included scope:

- local CLI
- local Python API
- local stdio MCP server (optional extra)
- schema validation
- rendering
- exports
- feeds
- sitemap
- assistant/skill prompt packs

Out of scope in v0.3.0:

- application forms and application collection
- CV upload and CV parsing
- candidate storage
- email delivery
- payments
- hosted APIs/frontends/infrastructure
- ATS workflows
- direct LinkedIn posting integrations

## Development

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run pytest -m integration
uv run python -m mkdocs build --strict
```

## Release and docs references

- Release notes: [`docs/project/release-notes.md`](docs/project/release-notes.md)
- Version policy: [`docs/project/versioning.md`](docs/project/versioning.md)
- Changelog: [`CHANGELOG.md`](CHANGELOG.md)
- LLM usage: [`docs/llm-usage.md`](docs/llm-usage.md)
- Scope boundaries: [`docs/roadmap-boundaries.md`](docs/roadmap-boundaries.md)
- Security policy: [`SECURITY.md`](SECURITY.md)

## Codebase docs index

- Core package: [`src/neksus_jobspec/README.md`](src/neksus_jobspec/README.md)
- App use cases: [`src/neksus_jobspec/app/README.md`](src/neksus_jobspec/app/README.md)
- JobSpec domain: [`src/neksus_jobspec/jobspec/README.md`](src/neksus_jobspec/jobspec/README.md)
- JobSpec vertical ops: [`src/neksus_jobspec/jobspec/spec_ops/README.md`](src/neksus_jobspec/jobspec/spec_ops/README.md)
- Rendering internals: [`src/neksus_jobspec/jobspec/rendering/README.md`](src/neksus_jobspec/jobspec/rendering/README.md)
- Project internals: [`src/neksus_jobspec/project/README.md`](src/neksus_jobspec/project/README.md)
- CLI package: [`src/neksus_jobspec_cli/README.md`](src/neksus_jobspec_cli/README.md)
- CLI commands: [`src/neksus_jobspec_cli/commands/README.md`](src/neksus_jobspec_cli/commands/README.md)
- MCP package: [`src/neksus_jobspec_mcp/README.md`](src/neksus_jobspec_mcp/README.md)

## License

Licensed under AGPL-3.0-or-later. See [LICENSE](LICENSE).

## Contribution policy

This repository is owner-maintained and does not use a public external
contribution workflow.
