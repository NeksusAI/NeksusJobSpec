# JobSpec Structure

A JobSpec is a YAML document validated against schema version `1`.

Schema version policy:
- `schema_version: 1` is the current and supported version.
- Future versions are currently rejected.
- Use `neksus-jobspec spec migrate PATH` to inspect migration status.

## Minimal valid example

```yaml
schema_version: 1
id: backend-engineer
title: Backend Engineer
summary: "Build backend services for employer workflows."
responsibilities:
  - "Design and implement backend APIs."
requirements:
  - "3+ years of backend software engineering experience."
nice_to_have: []
```

## Top-level fields

- `schema_version` (`int`, must be `1`)
- `id` (`str`, slug pattern)
- `title` (`str`, non-empty)
- `department` (`str | null`)
- `level` (`str | null`)
- `location` (`object | null`)
- `summary` (`str`, non-empty)
- `responsibilities` (`list[str]`, at least one non-empty string)
- `requirements` (`list[str]`, at least one non-empty string)
- `nice_to_have` (`list[str]`, optional)
- `employment` (`object | null`)

## Location

```yaml
location:
  type: remote # remote | hybrid | onsite
  city: null
  country: null
```

## Employment

```yaml
employment:
  type: full-time # full-time | part-time | contract | internship
```

## Warnings

Possible warning categories:
- short title
- duplicate responsibilities
- duplicate requirements
- hybrid/onsite role missing city and country
