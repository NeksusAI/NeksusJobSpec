# Installation

## Install from PyPI

```bash
pip install neksus-jobspec
```

## Verify installation

```bash
neksus-jobspec version
python -c "import neksus_jobspec; print(neksus_jobspec.__version__)"
```

## Local development setup

```bash
git clone https://github.com/NeksusAI/NeksusJobSpec.git
cd NeksusJobSpec
uv sync
```

## Install documentation dependencies

```bash
pip install -r requirements-docs.txt
```

## Serve docs locally

```bash
mkdocs serve
```

## Build docs locally

```bash
mkdocs build --strict
```

## Verify project setup

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run neksus-jobspec version
```

## Useful local commands

```bash
uv run pytest -q
uv run pytest tests/test_cli_spec_validate.py -x
uv run neksus-jobspec init
uv run neksus-jobspec check
```


## Smoke test

```bash
uv run pytest -m integration && uv run python -m mkdocs build --strict
```


## 3-layer local test run

```bash
uv run pytest -m "not integration"
uv run pytest -m integration && uv run python -m mkdocs build --strict
uv run pytest -m integration
```
