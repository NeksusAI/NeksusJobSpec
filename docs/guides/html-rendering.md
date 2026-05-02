# HTML Rendering

Neksus supports deterministic HTML output in addition to markdown.

## Render to stdout

```bash
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format html
```

## Render to file

```bash
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format html --output dist/backend-engineer.html
```

## Notes

- HTML renderer is template-free and semantic (`<main>`, `<section>`, headings, lists).
- Optional sections are omitted when empty.
- No PDF generation in this milestone.
