# Neksus JobSpec

Neksus JobSpec is an open-source, local-first CLI and Python package for creating, validating, and rendering structured job specifications written in YAML.

Documentation: https://docs.jobspec.neksusai.com/

Documentation can later be mapped to a custom domain through GitHub Pages settings and DNS.

## Status

Current focus is a stable CLI and reusable core library. Hosted API and MCP server capabilities are planned, not yet implemented.

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
