# Getting Started

Neksus JobSpec is for teams who want validated, machine-readable job campaign content without adopting hosted infrastructure.

## Core flow

```text
Write YAML -> Validate -> Lint -> Preview/Render -> Export/Feed/Sitemap
```

## Recommended first commands

```bash
neksus-jobspec doctor
neksus-jobspec init
neksus-jobspec spec new backend-engineer
neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml
neksus-jobspec spec lint jobspecs/backend-engineer.jobspec.yaml
neksus-jobspec spec preview jobspecs/backend-engineer.jobspec.yaml --no-open
```

## Then choose your path

- Need command-by-command walkthrough: [Quickstart](quickstart.md)
- Need exact command selection logic: [CLI Decision Guide](cli-decision-guide.md)
- Need schema-level details: [Specification](../concepts/specification.md)
- Need theme customization: [Custom Theme Package Guide](custom-theme-package.md)
