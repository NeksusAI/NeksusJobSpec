# Rendering

Neksus v0.2.x renders component-based JobSpecs to `web` and `json-ld`.

## Input model

Rendering expects a v0.2.x component JobSpec (`page` + `job` + `components`).

## Web

- Renders component order with explicit regions:
  - `.jobspec-fullwidth`
  - `.jobspec-main`
  - `.jobspec-sidebar`
- Maps components by `placement` (`fullwidth`, `main`, `sidebar`).
- Supports apply CTA, optional repeated CTA, share links, and print link.
- Supports `rendering.web.show_top_apply` to hide/show the top-level apply button.
- Supports CSS tokens and inline CSS.
- Supports `rendering.web.asset_base_url` (or CLI `--asset-base-url`) to prefix relative component media/asset URLs in generated HTML.
- Supports `rendering.web.labels` for localized action/contact labels (`share`, `print`, `phone`, `mobile`, `email`, `open_map`, `deadline`).
- Inline JS is not part of the default v0.2.x rendering contract.
- Print links are rendered without inline event-handler JavaScript.

## JSON-LD

- Outputs `schema.org` `JobPosting` JSON-LD from the validated model.

## Security boundaries

- CSS/JS settings are trusted local-output settings.
- Rendering emits output only; it does not execute scripts.
- Rendering does not fetch external resources.
