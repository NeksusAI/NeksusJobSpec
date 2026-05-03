# Python API

Stable public API is exposed from `neksus_jobspec`:

```python
from neksus_jobspec import JobSpec, load_jobspec, validate_jobspec, render_jobspec
```

See [API Reference](api-reference.md) and [Versioning and Compatibility Policy](versioning.md).

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
print(render_jobspec(spec, format="json"))
```
