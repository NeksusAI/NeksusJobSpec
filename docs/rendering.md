# Rendering

Neksus v0.2.x renders component-based JobSpecs to `web` and `json-ld`.

## Input model

Rendering expects a v0.2.x component JobSpec (`page` + `job` + `components`).

## Web

- Renders component order with explicit regions:
  - `.jobspec-region--header`
  - `.jobspec-region--hero`
  - `.jobspec-main`
  - `.jobspec-sidebar`
  - `.jobspec-region--footer`
- Maps components by `placement` (`fullwidth`, `main`, `sidebar`) and `region`.
- Supports apply CTA, optional repeated CTA, share links, and print link.
- Supports CSS tokens and inline CSS from YAML.
- Supports `rendering.web.asset_base_url` (or CLI `--asset-base-url`) to prefix relative component media/asset URLs.
- Supports built-in theme names via `--theme`.
- JSON-LD output remains model-driven.

## JSON-LD

- Outputs `schema.org` `JobPosting` JSON-LD from the validated model.

## Security boundaries

- CSS settings are trusted local-output settings.
- Rendering emits output only; it does not execute scripts.
- Rendering does not fetch external resources.
