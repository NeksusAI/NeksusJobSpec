# Neksus JobSpec

Neksus JobSpec is a local-first CLI and Python package for creating structured, branded, machine-readable job campaign pages from YAML.

Current docs target: **v0.4.x**.

## Start here

1. [Installation](guides/installation.md)
2. [First Run Checklist](guides/first-run-checklist.md)
3. [Quickstart](guides/quickstart.md)
4. [CLI Decision Guide](guides/cli-decision-guide.md)

## Product boundary

Neksus JobSpec free/core includes:
- local CLI
- local Python API
- local rendering/export/feed/sitemap
- optional local MCP server

It does **not** include hosted SaaS, authentication, database persistence, candidate collection, CV handling, payments, ATS workflow automation, or direct LinkedIn API posting.

See [Scope and Non-Goals](guides/scope-and-non-goals.md).

## Minimal example

```yaml
schema_version: 1
id: backend-engineer
page:
  layout: job_detail
job:
  title: Backend Engineer
  apply:
    method: external_url
    url: https://example.com/apply/backend-engineer
components:
  - type: hero
    id: hero
    title: Backend Engineer
  - type: list
    id: requirements
    items:
      - 3+ years of backend engineering experience.
```

## Common workflows

```bash
neksus-jobspec doctor
neksus-jobspec spec validate examples/startup-engineer.jobspec.yaml
neksus-jobspec spec lint examples/startup-engineer.jobspec.yaml
neksus-jobspec spec preview examples/startup-engineer.jobspec.yaml --no-open
neksus-jobspec themes list
```
