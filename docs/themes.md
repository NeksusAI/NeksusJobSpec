# Themes

Neksus renders `web` output with one built-in theme and optional CSS overrides.

## Built-in theme

List available themes:

```bash
neksus-jobspec themes
neksus-jobspec themes --json
```

Inspect theme metadata:

```bash
neksus-jobspec themes show soft-professional
```

Current built-in:

- `soft-professional`

Use it at render time:

```bash
neksus-jobspec spec render examples/danish-job-detail.jobspec.yaml --format web --theme soft-professional --output dist/danish-job-detail.html
```

## CSS customization

Layer your CSS on top of the embedded base theme:

```bash
neksus-jobspec spec render examples/danish-job-detail.jobspec.yaml --format web --theme soft-professional --css examples/jobspec.css --output dist/danish-job-detail-custom.html
```

Disable embedded base CSS (advanced):

```bash
neksus-jobspec spec render examples/danish-job-detail.jobspec.yaml --format web --no-css --css examples/jobspec.css
```

## Theme selection in JobSpec YAML

```yaml
rendering:
  web:
    template: soft-professional
```

`rendering.web.template` can be a built-in theme name (currently `soft-professional`).

Built-in theme CSS is file-based under:

- `neksus/core/jobspec/rendering/theme_css/soft-professional.css`
