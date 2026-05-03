# Python API

## Installation

```bash
pip install neksus-jobspec
```

## Stable imports

```python
from neksus_jobspec import JobSpec, load_jobspec, render_jobspec, validate_jobspec
```

## Load and validate

```python
from neksus_jobspec import load_jobspec, validate_jobspec

spec = load_jobspec("jobspecs/backend-engineer.jobspec.yaml")
validated = validate_jobspec(spec.model_dump())
```

## Render to string

```python
from neksus_jobspec import render_jobspec

markdown = render_jobspec("jobspecs/backend-engineer.jobspec.yaml", format="markdown")
html = render_jobspec("jobspecs/backend-engineer.jobspec.yaml", format="html", theme="modern")
```

## Render to file

```python
from neksus_jobspec import render_jobspec

render_jobspec(
    "jobspecs/backend-engineer.jobspec.yaml",
    format="html",
    theme="modern",
    output="dist/backend-engineer.html",
)
```

## Workflow note

The CLI remains the primary workflow. The Python API is stable for scripts, local automation, assistant tooling, and future MCP integration work.

Hosted API and MCP server implementations are planned, not available yet.
