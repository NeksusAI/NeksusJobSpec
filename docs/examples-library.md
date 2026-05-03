# Examples Library

This page provides component-based v0.2.0 examples.

## Minimal role

```yaml
schema_version: 1
id: office-assistant
page:
  layout: job_detail
job:
  title: Office Assistant
  intro: Support daily office operations.
components:
  - type: hero
    id: hero
    variant: default
    title: Office Assistant
    intro: Support daily office operations.
  - type: list
    id: requirements
    variant: bullets
    title: Requirements
    items:
      - Strong organizational skills.
```

## Technical role with facts and process

```yaml
schema_version: 1
id: data-platform-engineer
page:
  layout: job_detail
  component_order: [hero, facts, responsibilities, requirements, process]
job:
  title: Data Platform Engineer
components:
  - type: hero
    id: hero
    variant: split
    title: Data Platform Engineer
  - type: facts
    id: facts
    variant: sidebar
    items:
      - label: Region
        value: Copenhagen
  - type: list
    id: responsibilities
    variant: bullets
    title: Responsibilities
    items: [Build ETL jobs]
  - type: list
    id: requirements
    variant: bullets
    title: Requirements
    items: [Strong SQL skills]
  - type: application_process
    id: process
    variant: steps
    title: Application process
    steps: [Apply, Interview, Offer]
```

For a full production-style example, use `examples/danish-job-detail.jobspec.yaml`.
