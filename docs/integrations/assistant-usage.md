# Assistant Usage Guidance

## Preferred workflow

1. Produce typed JobSpec data.
2. Validate before render.
3. Render to JSON-LD for automation and web for presentation.

## Components-first guidance

For v0.3.x job-detail pages, assistants should prefer typed `components` over arbitrary HTML.

- Use only documented component types and variants.
- Do not invent unknown component types or variant names.
- If `page.component_order` is set, include each declared component ID exactly once.

## Security and trust boundaries

- Custom CSS is supported.
- Do not rely on JavaScript for theme behavior in v0.3.x.
- Rendering emits text output; it does not execute scripts.

## Automation recommendation

Prefer `--format json-ld` output for deterministic machine workflows.
