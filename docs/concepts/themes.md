# Themes

Neksus renders `web` output through built-in or filesystem custom theme packages.

## Theme discovery and inspection

```bash
neksus-jobspec themes list
neksus-jobspec themes show soft-professional
neksus-jobspec themes show examples/themes/minimal
```

Built-in themes:
- `classic`
- `classic-dark`
- `soft-professional`
- `custom` (filesystem package mode)

## Theme developer workflow

```bash
neksus-jobspec themes init my-theme
neksus-jobspec themes validate my-theme
neksus-jobspec spec render examples/startup-engineer.jobspec.yaml --format web --theme ./my-theme --output dist/startup-engineer-custom.html
```

## Package requirements

A custom theme directory must include:
- `manifest.json`
- template file declared by `manifest.template`
- CSS files declared by `manifest.styles`

Validation checks:
- manifest required fields
- known component and region names
- referenced template/CSS files exist
- mandatory component support
- render smoke test on a minimal valid JobSpec

## Render examples

### Soft-Professional

![Soft Professional Theme](../assets/soft-professional-current-render.png)

### Classic

![Classic Theme Render](../assets/classic-current-render.png)

### Classic-Dark

![Classic-Dark Theme Render](../assets/classic-dark-current-render.png)
