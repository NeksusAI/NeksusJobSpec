# Python API

Stable imports:

```python
from neksus_jobspec import JobSpec, load_jobspec, validate_jobspec, render_jobspec
```

This API targets the v0.4.x component schema (`page`, `job`, `components`).

## Example

```python
from neksus_jobspec import validate_jobspec, render_jobspec

data = {
    "schema_version": 1,
    "id": "backend-engineer",
    "page": {"layout": "job_detail"},
    "job": {
        "title": "Backend Engineer",
        "apply": {"method": "external_url", "url": "https://example.com/apply/backend-engineer"},
    },
    "components": [
        {"type": "hero", "id": "hero", "title": "Backend Engineer"},
        {"type": "list", "id": "requirements", "items": ["Python"]},
    ],
}

spec = validate_jobspec(data)
web = render_jobspec(spec, format="web")
jsonld = render_jobspec(spec, format="json-ld")
```
