# Assistant Usage Guidance

## Preferred workflow

1. Produce typed JobSpec data.
2. Validate before render.
3. Render to JSON-LD for automation and web/PDF for presentation.

## Components-first guidance

For v0.2.x job-detail pages, assistants should prefer typed `components` over arbitrary HTML.

- Use only documented component types and variants.
- Do not invent unknown component types or variant names.
- If `page.component_order` is set, include each declared component ID exactly once.

## Security and trust boundaries

- Custom CSS is supported.
- JS settings are trusted/local-only output controls.
- Inline JS must remain disabled unless explicitly allowed.
- Rendering emits text output; it does not execute scripts.

## Automation recommendation

Prefer `--format json-ld` output for deterministic machine workflows.
