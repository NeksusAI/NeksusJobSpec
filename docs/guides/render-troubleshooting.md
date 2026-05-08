# Render and Command Troubleshooting

## `doctor` reports FAIL

- Read the failed check row first.
- If importability fails, reinstall in a clean environment.
- If repository file checks fail, run from project root.

## `spec validate` fails

- Fix schema errors first.
- Use `spec schema --output ...` with editor integration for YAML validation.

## `spec lint` shows warnings

Warnings are advisory. Typical fixes:
- add `job.apply`
- use HTTPS apply URL
- add salary/location metadata (`meta_chips`)
- expand short intro text
- add campaign metadata

## `spec preview` fails to start

- Port conflict: choose another port (`--port 8770`).
- Invalid spec: run `spec validate` first.
- Stop preview with `Ctrl+C`.

## Custom theme validation fails

Run:

```bash
neksus-jobspec themes validate <theme-path>
```

Check:
- `manifest.json` exists and is valid JSON
- template file exists
- all CSS files in `styles` exist
- supported components/regions use known names

## Output looks wrong but validation passes

- Render once with a built-in theme to isolate content vs theme issues.
- Compare against `examples/startup-engineer.jobspec.yaml`.
- Verify `page.component_order` includes all component IDs exactly once when set.

## Export/feed/sitemap issues

- Ensure each input file passes `spec validate`.
- Confirm shell glob resolves to the files you expect.
- Use `--json` mode for machine-readable diagnostics where available.
