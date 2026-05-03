# Rendering

Neksus v0.2.0 renders component-based JobSpecs to `markdown`, `html`, and `json`.

## Input model

Rendering expects a v0.2.0 component-based JobSpec (`job` + `components`).

## Markdown

- Renders title/intro and component content in resolved order.
- Ignores visual-only styling variants.
- Does not render CSS or JS.

## HTML

- Renders component layout and preserves component order.
- Supports facts positioning via layout classes.
- Supports apply CTA, optional repeated CTA, share links, and print link.
- Supports CSS tokens, inline CSS, JS file includes.
- Inline JS is emitted only when `rendering.js.allow_inline: true`.
- Print links are rendered without inline event-handler JavaScript.

## JSON

- Outputs normalized validated payload with `page`, `job`, `components`, and `rendering`.

## Security boundaries

- CSS/JS settings are trusted local-output settings.
- Rendering emits output only; it does not execute scripts.
- Rendering does not fetch external resources.
