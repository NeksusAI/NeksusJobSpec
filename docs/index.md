# Neksus JobSpec

Neksus JobSpec is a local-first toolchain for component-based job-detail specifications.

Install:

```bash
pip install neksus-jobspec
```

## v0.3.x model

v0.3.x uses typed page components and is not backward compatible with legacy simple-schema JobSpec files.

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

- [Quickstart](guides/quickstart.md)
- [Specification](concepts/specification.md)
- [Schema](reference/schema.md)
- [Examples](guides/examples.md)
- [Python API](reference/python-api.md)
