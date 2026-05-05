# Getting Started

## Who this project is for

Neksus JobSpec is for teams and developers who want structured, portable hiring specs that can be validated and rendered consistently.

## Main use cases

- Create structured job descriptions in YAML
- Export to common output formats (Markdown, HTML, JSON)
- Feed LLM tools with normalized role data
- Prepare structured content for future ATS/job-board pipelines
- Keep an open-source foundation that can later support hosted API/server offerings

## Conceptual flow

```text
Write YAML -> Parse -> Validate -> Inspect -> Render -> Check project
```

1. Write a `*.jobspec.yaml` file.
2. Validate against JobSpec model rules.
3. Inspect normalized fields and metadata.
4. Render to output formats.
5. Run project-level checks for consistency and duplicate IDs.

## Command reference

Top-level command groups:

- `neksus-jobspec version`
- `neksus-jobspec init`
- `neksus-jobspec render`
- `neksus-jobspec spec ...`
- `neksus-jobspec check`
- `neksus-jobspec themes ...`
- `neksus-jobspec config ...`

For setup and command examples, continue with [Installation](installation.md) and [Quickstart](quickstart.md).
