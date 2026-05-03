# Assistant Usage Guidance

## Preferred workflow

1. Produce typed JobSpec data.
2. Validate before render.
3. Render to JSON for automation and Markdown/HTML for presentation.

## Components-first guidance

For v0.2.0 job-detail pages, assistants should prefer typed `components` over arbitrary HTML.

- Use only documented component types and variants.
- Do not invent unknown component types or variant names.
- Keep `page.component_order` aligned with declared component IDs.

## Security and trust boundaries

- Custom CSS is supported.
- JS settings are trusted/local-only output controls.
- Inline JS must remain disabled unless explicitly allowed.
- Rendering emits text output; it does not execute scripts.

## Automation recommendation

Prefer `--format json` output for deterministic machine workflows.
