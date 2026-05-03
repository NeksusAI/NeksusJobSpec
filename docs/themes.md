# Themes

Neksus renders `web` output with built-in themes and optional CSS overrides.

## Built-in themes

List available themes:

```bash
neksus-jobspec themes
neksus-jobspec themes --json
```

Inspect one theme:

```bash
neksus-jobspec themes show classic
```

Current built-ins:

- `default`
- `compact`
- `modern`
- `classic`

Use a theme at render time:

```bash
neksus-jobspec spec render examples/danish-job-detail.jobspec.yaml --format web --theme classic --output dist/danish-job-detail-classic.html
```

## CSS customization

You can layer CSS on top of built-ins:

```bash
neksus-jobspec spec render examples/danish-job-detail.jobspec.yaml --format web --theme classic --css examples/jobspec.css --output dist/danish-job-detail-custom.html
```

Disable built-in embedded CSS (advanced):

```bash
neksus-jobspec spec render examples/danish-job-detail.jobspec.yaml --format web --no-css --css examples/jobspec.css
```

## Theme selection in JobSpec

Set theme directly in spec:

```yaml
rendering:
  web:
    template: classic
```

Supported values for `rendering.web.template`:

- `default`
- `compact`
- `modern`
- `classic`
- `corporate`
- `minimal`

`corporate` and `minimal` are compatibility aliases to built-in style families.

## Custom template directory

Use a custom template directory path:

```bash
neksus-jobspec spec render examples/danish-job-detail.jobspec.yaml --format web --custom-template-dir ./my-template
```

Current contract (v0.2.x):

- Directory must exist.
- `template.yaml` must exist in that directory.
- If missing, render fails with a controlled error.

Minimal structure:

```text
my-template/
  template.yaml
```

Minimal manifest example:

```yaml
name: my-template
version: 1
```

Note: v0.2.x validates manifest presence only. Full custom-template slot/asset contracts are planned for a later release.
