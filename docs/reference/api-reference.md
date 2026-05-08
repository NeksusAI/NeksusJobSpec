# Public API Reference

Stable public imports:

```python
from neksus_jobspec import JobSpec, load_jobspec, validate_jobspec, render_jobspec, __version__
```

## `JobSpec`

Validated component-based model (`schema_version: 1`) used in v0.4.x.

## `load_jobspec(path)`

Loads YAML from disk and returns a validated `JobSpec`.

## `validate_jobspec(path_or_data)`

Validates a mapping or YAML path into `JobSpec`.

## `render_jobspec(spec_or_path, format="web", theme=None, asset_base_url=None)`

Renders a validated spec to `web` or `json-ld` text.

Notes:
- `theme` applies to web output.
- `asset_base_url` prefixes relative component asset URLs in web output.

## `__version__`

Package version string.

See [Versioning](../project/versioning.md) and [Python API](python-api.md).
