# Rendering

Neksus v0.2.x renders component-based JobSpecs to `web` and `json-ld`.

## Input model

Rendering expects a v0.2.x component JobSpec (`page` + `job` + `components`).

## Web

- Uses the built-in `soft-professional` HTML contract for component-based job-detail pages.
- Derives visible job content from YAML components and rendering config.
- Supports apply CTA, share links, and print-link icon toggle from `rendering.web`.
- Supports CSS overrides from CLI (`--css`) and YAML (`rendering.web.css`).
- Supports `rendering.web.asset_base_url` (or CLI `--asset-base-url`) to prefix relative component media/asset URLs.
- Supports built-in theme names via `--theme`.
- JSON-LD output remains model-driven.

See also:

- [Soft-Professional Guide](soft-professional-guide.md)
- [Content vs Theme](content-vs-theme.md)
- [Render Troubleshooting](render-troubleshooting.md)

## JSON-LD

- Outputs `schema.org` `JobPosting` JSON-LD from the validated model.

## Security boundaries

- CSS settings are trusted local-output settings.
- Rendering emits output only; it does not execute scripts.
- Rendering itself does not fetch external resources; rendered HTML may reference external assets (for example fonts/scripts/images).
