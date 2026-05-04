# Render Troubleshooting

## Output is missing section content

- Check component exists in `components`.
- Check component `id` appears in `page.component_order` when order is set.
- Check `visibility` / `render_if` rules are not hiding it.

## Wrong text appears in hero chips

- Validate `meta_chips.items[*].label` contains expected keywords:
  - location: `Location`
  - salary: `Salary` or `Comp`
  - type: `Type` or `Employment`

## Map image or label is wrong

- Image source priority:
  1. `hero_banner.image_url`
  2. `location_map.map_url`
- Label source: `location_map.address`

## Footer icons not visible

- Add `social_links.links[*].icon` values.
- Or enable rendering toggles:
  - `rendering.web.show_share_links: true`
  - `rendering.web.show_print_link: true`

## CSS overrides do nothing

- Confirm file path passed to `--css` exists.
- Verify selector specificity; override classes may require stronger selectors.
- Confirm rendered output includes `<style>` block and override rules.

## Relative assets break after deploy

- Set `rendering.web.asset_base_url` in YAML, or
- pass `--asset-base-url` during render.

## Validation passes but output still looks off

- Compare with `examples/job-detail.jobspec.yaml`.
- Render with no custom CSS first.
- Then re-add `--css` overrides incrementally.
