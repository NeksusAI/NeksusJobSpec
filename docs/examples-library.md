# Examples Library

This page provides scenario-focused examples beyond the quick examples page.

## Minimal role

```yaml
schema_version: 1
id: office-assistant
title: Office Assistant
summary: Support daily office operations and coordination.
responsibilities:
  - Coordinate office supplies.
requirements:
  - Strong organizational skills.
```

## Technical role

```yaml
schema_version: 1
id: data-platform-engineer
title: Data Platform Engineer
department: Engineering
summary: Build data pipelines and platform services.
responsibilities:
  - Build ETL jobs.
  - Maintain data observability tooling.
requirements:
  - 4+ years of backend or data engineering experience.
  - Strong SQL skills.
employment:
  type: full-time
location:
  type: hybrid
  city: Copenhagen
  country: Denmark
```

## Non-technical role

```yaml
schema_version: 1
id: customer-success-manager
title: Customer Success Manager
summary: Drive customer onboarding, adoption, and retention.
responsibilities:
  - Lead customer onboarding plans.
  - Run quarterly business reviews.
requirements:
  - Experience in B2B customer success.
employment:
  type: full-time
location:
  type: remote
```

## Location variants

Remote:

```yaml
location:
  type: remote
```

Hybrid:

```yaml
location:
  type: hybrid
  city: Copenhagen
  country: Denmark
```

Onsite:

```yaml
location:
  type: onsite
  city: Aarhus
  country: Denmark
```

## Warning-trigger examples

Very short title (warning):

```yaml
title: Dev
```

Duplicate responsibilities (warning):

```yaml
responsibilities:
  - Build APIs.
  - build apis.
```

Hybrid role with missing city/country (warning):

```yaml
location:
  type: hybrid
```

## Corrected versions

Use descriptive title:

```yaml
title: Backend Engineer
```

Remove duplicate task statements:

```yaml
responsibilities:
  - Build APIs.
  - Maintain API reliability.
```

Add location detail for hybrid/onsite:

```yaml
location:
  type: hybrid
  city: Copenhagen
  country: Denmark
```
