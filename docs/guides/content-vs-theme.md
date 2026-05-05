# Content vs Theme

Use this split to decide where a change belongs.

| Concern | Put it in |
|---|---|
| Job title, role copy, requirements, salary/location/type values | JobSpec YAML (`job`, `components`) |
| CTA labels and contact fields | JobSpec YAML (`job.apply`, `meta_panel`, `rendering.web.labels`) |
| Map URL/address/alt text | JobSpec YAML (`hero_banner`, `location_map`) |
| Page spacing, colors, typography, borders, responsive layout rules | Theme CSS |
| Head includes (font/script links) and HTML scaffold contract | Renderer/theme implementation |
| One-off organization branding tweaks across many specs | Custom CSS file + `--css` |

## Rule of thumb

- If users read it as business content, put it in YAML.
- If it controls look/feel/system styling, keep it in theme CSS or renderer contract.
