# Examples Library

This page provides focused snippets for common user scenarios in v0.4.x.

## Minimal valid spec

```yaml
schema_version: 1
id: office-assistant
page:
  layout: job_detail
job:
  title: Office Assistant
  apply:
    method: external_url
    url: https://example.com/apply/office-assistant
components:
  - type: hero
    id: hero
    title: Office Assistant
  - type: list
    id: requirements
    items:
      - Strong organizational skills.
```

## Campaign-active spec

```yaml
campaign:
  starts_at: 2026-05-04
  expires_at: 2026-07-03
  status: active
```

## Campaign-closed spec

```yaml
campaign:
  status: closed
```

## Onsite/hybrid hint with structured location

```yaml
components:
  - type: meta_chips
    id: chips
    items:
      - label: Workplace
        value: Hybrid
      - label: Location
        value: Copenhagen, Denmark
        semantic: location
```

## Recommended command checks for any example

```bash
neksus-jobspec spec validate <path>
neksus-jobspec spec lint <path>
neksus-jobspec spec status <path>
```
