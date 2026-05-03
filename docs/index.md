# Neksus JobSpec

Neksus JobSpec is a local-first toolchain for component-based job-detail specifications.

Install:

```bash
pip install neksus-jobspec
```

## v0.2.0 model

v0.2.0 uses typed page components and is not backward compatible with v0.1.0 legacy top-level content files.

## Short example

```yaml
schema_version: 1
id: backend-engineer
page:
  layout: job_detail
job:
  title: Backend Engineer
  intro: Build backend services for employer workflows.
components:
  - type: hero
    id: hero
    variant: default
    title: Backend Engineer
    intro: Build backend services for employer workflows.
  - type: list
    id: requirements
    variant: bullets
    title: Requirements
    items:
      - 3+ years of backend software engineering experience.
```

## Next steps

- [Quickstart](quickstart.md)
- [Specification](specification.md)
- [Schema](schema.md)
- [Examples](examples.md)
- [Python API](python-api.md)
