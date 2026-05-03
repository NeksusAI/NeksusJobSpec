# Examples

## Example 1: Simple job post (YAML)

```yaml
schema_version: 1
id: support-specialist
title: Support Specialist
summary: Help customers resolve onboarding and product usage issues.
responsibilities:
  - Respond to customer support requests.
  - Document common troubleshooting paths.
requirements:
  - Strong written communication skills.
  - 1+ years in customer-facing support.
nice_to_have:
  - Experience with ticketing systems.
employment:
  type: full-time
location:
  type: remote
  city: null
  country: null
```

## Example 2: Structured technical role (YAML)

```yaml
schema_version: 1
id: platform-backend-engineer
title: Platform Backend Engineer
department: Engineering
level: Senior
summary: Build and operate backend platform services used across product teams.
responsibilities:
  - Design reliable internal APIs and event-driven workflows.
  - Improve observability and incident response runbooks.
  - Review architecture proposals for platform changes.
requirements:
  - 5+ years of backend software engineering experience.
  - Experience with distributed systems and SQL data modeling.
  - Strong testing and debugging discipline.
nice_to_have:
  - Experience with Python packaging and CLI tooling.
  - Experience with cloud infrastructure automation.
employment:
  type: full-time
location:
  type: hybrid
  city: Copenhagen
  country: Denmark
```

## Example rendered outputs

```bash
neksus-jobspec spec render jobspecs/platform-backend-engineer.jobspec.yaml --format markdown
neksus-jobspec spec render jobspecs/platform-backend-engineer.jobspec.yaml --format html --theme modern
neksus-jobspec spec render jobspecs/platform-backend-engineer.jobspec.yaml --format json
```

For more scenarios (non-technical roles, location variants, warning-trigger examples), see [Examples Library](examples-library.md).
