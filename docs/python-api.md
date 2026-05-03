# Python API

Stable public API is exposed from `neksus_jobspec`:

```python
from neksus_jobspec import JobSpec, load_jobspec, validate_jobspec, render_jobspec
```

See [API Reference](api-reference.md) and [Versioning and Compatibility Policy](versioning.md).

v0.2.x accepts the component schema (`page`, `job`, `components`) and no longer accepts legacy simple-schema payloads.

## Component page example

```python
from neksus_jobspec import validate_jobspec, render_jobspec

data = {
    "schema_version": 1,
    "id": "backend-engineer",
    "page": {"layout": "job_detail"},
    "job": {"title": "Backend Engineer", "intro": "Build reliable systems."},
    "components": [
        {
            "type": "list",
            "id": "requirements",
            "variant": "bullets",
            "title": "Requirements",
            "items": ["Python"],
        }
    ],
}

spec = validate_jobspec(data)
print(render_jobspec(spec, format="json-ld"))

# If your web output references relative media paths, prefix them at render time:
web = render_jobspec(spec, format="web", asset_base_url="../examples/assets")
```
