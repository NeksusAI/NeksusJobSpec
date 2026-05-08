# Installation

## Install from PyPI

```bash
pip install neksus-jobspec
```

Optional MCP extra:

```bash
pip install "neksus-jobspec[mcp]"
```

## If pip install fails in managed Python environments

Some systems block global pip installs (PEP 668). Use one of:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install neksus-jobspec
```

or with uv-managed environments:

```bash
uv sync
uv run neksus-jobspec --help
```

## Verify installation

```bash
neksus-jobspec version
neksus-jobspec doctor
python3 -c "import neksus_jobspec; print(neksus_jobspec.__version__)"
```

## Local development setup

```bash
git clone https://github.com/NeksusAI/NeksusJobSpec.git
cd NeksusJobSpec
uv sync
```

## Docs local build

```bash
pip install -r requirements-docs.txt
mkdocs build --strict
```
