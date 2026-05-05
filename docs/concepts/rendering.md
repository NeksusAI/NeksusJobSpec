# Rendering

Neksus v0.3.x renders component-based JobSpecs to `web` and `json-ld`.

## Input model

Rendering expects a v0.3.x component JobSpec (`page` + `job` + `components`).

## Web

- Uses built-in HTML contracts for `soft-professional`, `classic`, and `classic-dark` themes.
- Supports filesystem custom theme packages (`manifest.json` + Jinja template + CSS assets).
- Derives visible job content from YAML components and rendering config.
- Supports apply CTA, share links, and print-link icon toggle from `rendering.web`.
- Supports CSS overrides from CLI (`--css`) for built-in themes.
- Custom theme packages own their full visual contract through package template/CSS assets.
- Supports `rendering.web.asset_base_url` (or CLI `--asset-base-url`) to prefix relative component media/asset URLs.
- Supports built-in theme names via `--theme`.
- JSON-LD output remains model-driven.

See also:

- [Soft-Professional Guide](../guides/soft-professional-guide.md)
- [Classic Theme Guide](../guides/classic-guide.md)
- [Classic-Dark Theme Guide](../guides/classic-dark-guide.md)
- [Content vs Theme](../guides/content-vs-theme.md)
- [Render Troubleshooting](../guides/render-troubleshooting.md)

## JSON-LD

- Outputs `schema.org` `JobPosting` JSON-LD from the validated model.
- `campaign.expires_at` maps to `validThrough` when present.
- `campaign.starts_at` maps to `datePosted` when present.

## Campaign status rendering

- Jobs with `campaign.status: closed` or `campaign.status: expired` still render.
- Web output includes a visible status notice.
- Apply CTA remains visible but de-emphasized for closed/expired campaigns.

## Security boundaries

- CSS settings are trusted local-output settings.
- Rendering emits output only; it does not execute scripts.
- Rendering itself does not fetch external resources; rendered HTML may reference external assets (for example fonts/scripts/images).
