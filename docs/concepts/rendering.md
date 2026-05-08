# Rendering

Neksus renders validated component-based JobSpecs to:
- `web`
- `json-ld`

## Single-file rendering

```bash
neksus-jobspec spec render examples/startup-engineer.jobspec.yaml --format web --output dist/startup-engineer.html
neksus-jobspec spec render examples/startup-engineer.jobspec.yaml --format json-ld --output dist/startup-engineer.jsonld
```

## Local preview

```bash
neksus-jobspec spec preview examples/startup-engineer.jobspec.yaml --theme soft-professional --port 8765 --no-open
```

Use preview for fast local visual iteration; use render for reproducible build artifacts.

## Campaign status rendering

- Closed or expired campaigns still render.
- Web output can include visible campaign status notice.

## Theme selection

- Built-in: `soft-professional`, `classic`, `classic-dark`
- Custom: pass a theme package path and validate with `themes validate` first.
