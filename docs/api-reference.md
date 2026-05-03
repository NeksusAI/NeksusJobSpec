# Public API Reference

This page documents the stable public Python API.

```python
from neksus_jobspec import JobSpec, load_jobspec, validate_jobspec, render_jobspec, __version__
```

See [Versioning and Compatibility Policy](versioning.md).

## `JobSpec`

Purpose: validated v0.2.x component-based JobSpec model.

## `load_jobspec(path)`

Purpose: load YAML file and validate into `JobSpec`.

Arguments: `path: str | pathlib.Path`

Returns: `JobSpec`

Raises: `FileSystemError`, `JobSpecParseError`, `JobSpecValidationError`

## `validate_jobspec(path_or_data)`

Purpose: validate mapping data or a YAML path.

Arguments: `str | pathlib.Path | Mapping[str, Any]`

Returns: `JobSpec`

Raises: `FileSystemError`, `JobSpecParseError`, `JobSpecValidationError`

Example:

```python
from neksus_jobspec import validate_jobspec

spec = validate_jobspec(
    {
        "schema_version": 1,
        "id": "backend-engineer",
        "page": {"layout": "job_detail"},
        "job": {"title": "Backend Engineer"},
        "components": [
            {
                "type": "list",
                "id": "requirements",
                "variant": "bullets",
                "title": "Requirements",
                "items": ["Python experience"],
            }
        ],
    }
)
```

## `render_jobspec(spec_or_path, format="web", theme=None, output=None, css=None, asset_base_url=None)`

Purpose: render validated JobSpec as web/json-ld.

Arguments:
- `spec_or_path: JobSpec | str | pathlib.Path`
- `format: "web" | "json-ld"`
- `theme: str | None`
- `output: str | pathlib.Path | None`
- `css: str | None`
- `asset_base_url: str | None`

Returns: `str`

Raises: `FileSystemError`, `UnsupportedFormatError`, `JobSpecParseError`, `JobSpecValidationError`

## `__version__`

Purpose: package version string.
