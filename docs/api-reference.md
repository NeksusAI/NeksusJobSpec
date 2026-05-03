# Public API Reference

This page documents the stable public Python API.

Import from `neksus_jobspec`:

```python
from neksus_jobspec import JobSpec, load_jobspec, validate_jobspec, render_jobspec, __version__
```

See the [Versioning and Compatibility Policy](versioning.md) for contract scope.

Internal modules are intentionally not part of the compatibility contract.

## `JobSpec`

Purpose:
- Canonical validated JobSpec model for Python workflows.

Accepted arguments:
- Constructed via Pydantic validation or helper functions.

Return value:
- `JobSpec` model instance.

Example:

```python
from neksus_jobspec import validate_jobspec

spec = validate_jobspec({...})
print(spec.id)
```

## `load_jobspec(path)`

Purpose:
- Load YAML from disk and return a validated `JobSpec`.

Accepted arguments:
- `path`: `str | pathlib.Path`

Return value:
- `JobSpec`

Raises:
- `FileSystemError` when file access fails.
- `JobSpecParseError` when YAML is invalid.
- `JobSpecValidationError` when schema validation fails.

Example:

```python
from neksus_jobspec import load_jobspec

spec = load_jobspec("jobspecs/backend-engineer.jobspec.yaml")
```

## `validate_jobspec(path_or_data)`

Purpose:
- Validate either a file path or mapping data into a `JobSpec`.

Accepted arguments:
- `path_or_data`: `str | pathlib.Path | Mapping[str, Any]`

Return value:
- `JobSpec`

Raises:
- `FileSystemError` for file access failures.
- `JobSpecParseError` for invalid YAML when validating by path.
- `JobSpecValidationError` for invalid data.

Example:

```python
from neksus_jobspec import validate_jobspec

spec = validate_jobspec(
    {
        "schema_version": 1,
        "id": "backend-engineer",
        "title": "Backend Engineer",
        "summary": "Build backend systems.",
        "responsibilities": ["Build APIs"],
        "requirements": ["Python experience"],
    }
)
```

## `render_jobspec(spec_or_path, format="markdown", theme=None, output=None, css=None)`

Purpose:
- Render a validated JobSpec as markdown, html, or json.

Accepted arguments:
- `spec_or_path`: `JobSpec | str | pathlib.Path`
- `format`: `"markdown" | "html" | "json"`
- `theme`: `str | None`
- `output`: `str | pathlib.Path | None`
- `css`: `str | None`

Return value:
- `str` rendered content.

Raises:
- `FileSystemError` when writing output fails.
- `UnsupportedFormatError` for unsupported render formats.
- `JobSpecParseError` / `JobSpecValidationError` if loading from path fails.

Examples:

```python
from neksus_jobspec import render_jobspec

markdown = render_jobspec("jobspecs/backend-engineer.jobspec.yaml")
html = render_jobspec("jobspecs/backend-engineer.jobspec.yaml", format="html", theme="modern")
render_jobspec("jobspecs/backend-engineer.jobspec.yaml", output="dist/backend-engineer.md")
```

## `__version__`

Purpose:
- Package version string for diagnostics and automation.

Return value:
- `str`

Example:

```python
import neksus_jobspec

print(neksus_jobspec.__version__)
```

TODO: Future: generate this page from public API docstrings once the API surface is finalized.
