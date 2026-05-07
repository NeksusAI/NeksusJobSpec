# Custom Theme Package Guide

Use this guide to build a custom web theme package for Neksus JobSpec.

The renderer is theme-package-only:

- no runtime `--css` overrides
- no Python-side theme branches
- all styling/layout lives in your package assets

## 1. Create the package folder

Example:

```text
my-theme/
  manifest.json
  template.html.j2
  theme.css
```

## 2. Add `manifest.json`

Minimal valid example:

```json
{
  "name": "my-theme",
  "version": 1,
  "template": "template.html.j2",
  "styles": ["theme.css"],
  "supported_components": [
    "header_brand",
    "nav_links",
    "header_actions",
    "hero_banner",
    "hero",
    "meta_chips",
    "rich_text",
    "feature_grid",
    "list",
    "quote",
    "benefits",
    "application_process",
    "company_profile",
    "legal",
    "meta_panel",
    "social_links",
    "location_map"
  ],
  "supported_regions": ["header", "hero", "main", "sidebar", "footer"]
}
```

Notes:

- `template` must exist in the package.
- Every file in `styles` must exist in the package.
- `supported_components` and `supported_regions` must use known built-in names only.
- Theme manifests must support the global mandatory component set.

## 3. Add `template.html.j2`

Templates receive the render contract as `contract` and CSS bundle as `theme_css`.

Minimal example:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{ contract.title }}</title>
    <style>{{ theme_css }}</style>
  </head>
  <body>
    <header>{{ contract.spec_id }}</header>
    <main>
      <h1>{{ contract.title }}</h1>
      {% if contract.intro %}<p>{{ contract.intro }}</p>{% endif %}
    </main>
  </body>
</html>
```

## 4. Use the contract fields

Common contract fields:

- `contract.spec_id`
- `contract.schema_version`
- `contract.title`, `contract.intro`
- `contract.apply_label`, `contract.apply_url`, `contract.apply_method`
- `contract.campaign_status`
- `contract.theme`
- `contract.asset_base_url`
- `contract.sections`
- `contract.labels`
- `contract.show_top_apply`, `contract.show_share_links`, `contract.show_print_link`, `contract.repeat_cta`
- `contract.theme_config`
- `contract.mandatory` (`required`, `present`, `missing`)
- `contract.components`
- `contract.components_by_region`
- `contract.component_groups`

Component payload access example:

```jinja2
{% set hero = contract.component_groups.get('hero', []) %}
{% if hero %}
  <h1>{{ hero[0].payload.title }}</h1>
{% endif %}
```

## 5. Put style/layout in `theme.css`

All visual customization should live in the theme package CSS and template.

## 6. Render with your package

```bash
neksus-jobspec spec render examples/job-detail.jobspec.yaml \
  --format web \
  --theme ./my-theme \
  --output dist/job-detail-custom.html
```

## 7. Use YAML `theme_config` for theme knobs

Add theme-specific options in JobSpec YAML:

```yaml
rendering:
  web:
    theme_config:
      cta_title: "Questions?"
      icon_map:
        logo: "work"
```

Template reads these from `contract.theme_config`.

## 8. Validate failures quickly

If render fails, check:

- missing `manifest.json`
- missing `template.html.j2`
- missing CSS files declared in `styles`
- unsupported component/region names in manifest
- manifest missing mandatory component support
- JobSpec contains component types your manifest does not support

## Reference package

See sample package:

- `fixtures/themes/custom-basic/manifest.json`
- `fixtures/themes/custom-basic/template.html.j2`
- `fixtures/themes/custom-basic/theme.css`
