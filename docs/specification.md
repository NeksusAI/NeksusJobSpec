# JobSpec Format

Neksus v0.2.0 uses a component-based JobSpec schema for job-detail pages.

## Breaking compatibility note

`0.2.0` is not backward compatible with `0.1.0` JobSpec files that use legacy top-level content fields as the primary model.

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

## Ordering rules

- Component IDs must be unique per file.
- `page.component_order` must only reference existing component IDs.

## Security notes

- Typed components are the default authoring model.
- Arbitrary HTML is not the default model.
- Custom CSS is supported.
- JS config is trusted/local-only and inline JS requires explicit allow.
