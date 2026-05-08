# CLI Decision Guide

Use this page when you are unsure which command to run.

## Validate vs Lint

- Use `spec validate` when you need schema correctness and exit-code failure on invalid specs.
- Use `spec lint` when you want quality warnings that do not fail valid specs.

## Render vs Preview

- Use `spec render` when you need reproducible output files.
- Use `spec preview` when you need a quick local browser view while editing content.

## Status vs Inspect

- Use `spec status` for campaign and quality-warning context.
- Use `spec inspect` for normalized metadata summary.

## Themes commands

- `themes list`: discover available built-in themes.
- `themes show <name|path>`: inspect built-in theme metadata or custom package metadata.
- `themes init <target>`: scaffold a minimal custom theme.
- `themes validate <path>`: check manifest/template/assets + render smoke test.

## Single-job exports vs feeds

- `spec export`: one JobSpec into one target format.
- `feed export`: many JobSpecs into one feed artifact.
- `feed sitemap`: generate `sitemap.xml` for discoverability.

## Fast troubleshooting

- Run `doctor` first for environment/setup issues.
- Run `spec validate` before `spec render` or exports.
- Use `render-troubleshooting` for output/layout issues.
