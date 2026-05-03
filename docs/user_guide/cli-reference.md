# CLI Reference

Neksus JobSpec provides a command-line interface with these command groups:

- `neksus-jobspec version`
- `neksus-jobspec init`
- `neksus-jobspec render`
- `neksus-jobspec spec ...`
- `neksus-jobspec check`
- `neksus-jobspec themes ...`
- `neksus-jobspec config ...`

## `neksus-jobspec version`

Show installed CLI version.

## `neksus-jobspec init`

Initialize project folders and config.

Options:
- `--empty`
- `--force`
- `--json`

## `neksus-jobspec spec new NAME`

Create a new spec file.

Options:
- `--template {basic,engineering,product,sales}`
- `--output PATH`
- `--force`
- `--json`

## `neksus-jobspec spec validate PATH`

Validate a spec file.

Options:
- `--strict`
- `--json`

## `neksus-jobspec spec render PATH`

Render a spec file.

Options:
- `--format {markdown,html,json}`
- `--theme {default,compact,modern}`
- `--css PATH` (html only)
- `--no-css` (html only)
- `--output PATH`
- `--no-validate`
- `--json`

## `neksus-jobspec spec templates`

List built-in templates.

Options:
- `--json`

## `neksus-jobspec spec schema`

Export JSON Schema.

Options:
- `--output PATH`
- `--json`

## `neksus-jobspec spec inspect PATH`

Inspect normalized metadata.

Options:
- `--json`

## `neksus-jobspec spec migrate PATH`

Inspect schema-version migration status.

Options:
- `--write` (reserved; currently not implemented)
- `--json`

## `neksus-jobspec render`

Render all `*.jobspec.yaml` files in the configured project `spec_directory`.

Options:
- `--all` (alias/no-op)
- `--format {markdown,html,json}`
- `--theme {default,compact,modern}`
- `--profile NAME`
- `--css PATH` (html only)
- `--no-css` (html only)
- `--clean`
- `--json`

## `neksus-jobspec check`

Run project checks.

Options:
- `--strict`
- `--format {human,github}`
- `--json`

## `neksus-jobspec config get [KEY]`

Read config value(s).

Options:
- `--json`

## `neksus-jobspec config set KEY VALUE`

Update mutable config key.

Options:
- `--json`


## `neksus-jobspec themes`

List built-in render themes.

Options:
- `--json`

## `neksus-jobspec themes show NAME`

Show metadata for one built-in theme.

Options:
- `--json`
