# HTML Rendering

Neksus supports deterministic HTML output with built-in themes.

## Render to stdout

```bash
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format html --theme modern
```

## Render to file

```bash
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format html --output dist/backend-engineer.html
```

## Custom CSS

```bash
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format html --theme modern --css examples/jobspec.css
```

Custom CSS is appended after built-in theme CSS.

## Disable embedded CSS

```bash
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format html --no-css
```

This emits semantic HTML without a style block.

## Notes

- Theme choices are built-in: `default`, `compact`, `modern`.
- HTML renderer is template-free and semantic (`<main>`, `<section>`, headings, lists).
- CSS flags (`--css`, `--no-css`) are only valid for HTML output.
- JobSpec content remains HTML-escaped.
- No plugins, arbitrary templates, PDF, or DOCX in this phase.
