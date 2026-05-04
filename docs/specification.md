# JobSpec Format

Neksus v0.2.x uses a component-based JobSpec schema for job-detail pages.

## Breaking compatibility note

`0.2.x` is not backward compatible with `0.1.0` or transitional early `0.2.0` legacy-style payloads.
Legacy top-level content fields are removed from the accepted schema.

## Required top-level fields

- `schema_version`
- `id`
- `page`
- `job`
- `components`
- optional `rendering`

## Components model

`components` are typed, validated building blocks.

Shared fields:

- `type`
- `id`
- optional `variant`
- optional `title`
- optional `class_name`
- optional `attributes`
- optional `visibility`
- optional `render_if`
- `placement`: `main | sidebar | fullwidth`
- optional `container`

Supported component types:

- `hero`
- `facts`
- `rich_text`
- `list`
- `quote`
- `benefits`
- `contact`
- `company_profile`
- `legal`
- `cta`
- `media`
- `application_process`
- `header_brand`
- `hero_banner`
- `meta_panel`
- `social_links`
- `location_map`
- `footer_brand`
- `nav_links`
- `header_actions`
- `feature_grid`
- `meta_chips`

## Ordering rules

- Component IDs must be unique per file.
- If `page.component_order` is set, it must include each component ID exactly once.

## Security notes

- Typed components are the default authoring model.
- Arbitrary HTML is not the default model.
- Custom CSS is supported.
- Theme customization is CSS-first in v0.2.x.
- URL fields accept only safe schemes (`http`, `https`, `mailto`, `tel`) or safe relative paths.
- Component `attributes` are restricted to safe keys (`data-*`, `aria-*`, `id`, `role`, `title`).

## Web rendering knobs

`rendering.web` supports:

- `facts_position`: `sidebar | topbar | grid`
- `repeat_cta`: boolean
- `show_top_apply`: boolean
- `show_share_links`: boolean
- `show_print_link`: boolean
- `asset_base_url`: optional URL/path prefix for relative component asset URLs
- `labels`: optional localized UI labels:
  - `share`, `print`, `phone`, `mobile`, `email`, `open_map`, `deadline`
- `template`: built-in theme name or custom template identifier/path
