# Developer Setup

## Prerequisites

- Python 3.11+
- `uv` (recommended)

## Setup

```bash
git clone https://github.com/stefanrobertstegaru/NeksusJobSpec.git
cd NeksusJobSpec
uv sync
```

## Verify setup

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run neksus-jobspec version
```

## Useful commands

```bash
uv run pytest -q
uv run pytest tests/test_cli_spec_validate.py -x
uv run neksus-jobspec init
uv run neksus-jobspec check
```
