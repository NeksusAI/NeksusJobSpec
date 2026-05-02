# CLI Reference

Neksus JobSpec provides a command-line interface with these command groups:

- `neksus-jobspec version`
- `neksus-jobspec init`
- `neksus-jobspec spec ...`
- `neksus-jobspec check`
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
- `--format {markdown,html}`
- `--output PATH`
- `--no-validate`
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

## `neksus-jobspec check`

Run project checks.

Options:
- `--strict`
- `--json`

## `neksus-jobspec config get [KEY]`

Read config value(s).

Options:
- `--json`

## `neksus-jobspec config set KEY VALUE`

Update mutable config key.

Options:
- `--json`
