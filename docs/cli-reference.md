# CLI Reference

Use `neksus-jobspec --help` and `neksus-jobspec <command> --help` for inline help.

## `version`

Purpose: Show installed CLI version.

Syntax:

```bash
neksus-jobspec version [--json]
```

Options:

- `--json`: Emit machine-readable JSON.

Examples:

```bash
neksus-jobspec version
neksus-jobspec version --json
```

JSON notes: `--json` returns `{ "name": "neksus-jobspec", "version": "..." }`.

## `init`

Purpose: Initialize a project in current directory.

Syntax:

```bash
neksus-jobspec init [--empty] [--force] [--json]
```

Options:

- `--empty`: Skip creating example JobSpec.
- `--force`: Overwrite existing project config/example files.
- `--json`: Emit machine-readable JSON.

Examples:

```bash
neksus-jobspec init
neksus-jobspec init --empty
neksus-jobspec init --force --json
```

## `spec new`

Purpose: Create a new JobSpec file from a template.

Syntax:

```bash
neksus-jobspec spec new NAME [--template TEMPLATE] [--output PATH] [--force] [--json]
```

Options:

- `--template`: One of built-in templates.
- `--output`: Write to explicit path.
- `--force`: Overwrite if target exists.
- `--json`: Emit machine-readable JSON.

Examples:

```bash
neksus-jobspec spec new backend-engineer
neksus-jobspec spec new sales-lead --template sales
neksus-jobspec spec new product-manager --output jobspecs/pm.jobspec.yaml --json
```

## `spec validate`

Purpose: Validate one JobSpec file.

Syntax:

```bash
neksus-jobspec spec validate PATH [--strict] [--json]
```

Options:

- `--strict`: Treat warnings as failures.
- `--json`: Emit machine-readable JSON.

Examples:

```bash
neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml
neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml --strict
neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml --json
```

## `spec render`

Purpose: Render one JobSpec into markdown/html/json.

Syntax:

```bash
neksus-jobspec spec render PATH [--format FORMAT] [--theme THEME] [--css PATH] [--no-css] [--output PATH] [--no-validate] [--json]
```

Options:

- `--format`: `markdown`, `html`, `json`.
- `--theme`: Built-in render theme.
- `--css`: Append custom CSS (HTML only).
- `--no-css`: Disable embedded CSS (HTML only).
- `--output`: Write rendered content to file.
- `--no-validate`: Skip validation before rendering.
- `--json`: Emit machine-readable JSON.

Examples:

```bash
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format markdown
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format html --theme modern --css examples/jobspec.css
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format json --output dist/backend-engineer.json --json
```

JSON notes: includes render metadata and either `content` (stdout mode) or `output` path (file mode).

## `spec templates`

Purpose: List built-in templates.

Syntax:

```bash
neksus-jobspec spec templates [--json]
```

Options:

- `--json`: Emit machine-readable JSON.

Examples:

```bash
neksus-jobspec spec templates
neksus-jobspec spec templates --json
```

## `spec schema`

Purpose: Export JobSpec JSON Schema.

Syntax:

```bash
neksus-jobspec spec schema [--output PATH] [--json]
```

Options:

- `--output`: Write schema to file.
- `--json`: Emit machine-readable JSON.

Examples:

```bash
neksus-jobspec spec schema
neksus-jobspec spec schema --output schemas/jobspec.v1.json
neksus-jobspec spec schema --json
```

## `spec inspect`

Purpose: Inspect normalized JobSpec metadata.

Syntax:

```bash
neksus-jobspec spec inspect PATH [--json]
```

Options:

- `--json`: Emit machine-readable JSON.

Examples:

```bash
neksus-jobspec spec inspect jobspecs/backend-engineer.jobspec.yaml
neksus-jobspec spec inspect jobspecs/backend-engineer.jobspec.yaml --json
```

## `spec migrate`

Purpose: Inspect schema-version migration status.

Syntax:

```bash
neksus-jobspec spec migrate PATH [--write] [--json]
```

Options:

- `--write`: Reserved, currently not implemented.
- `--json`: Emit machine-readable JSON.

Examples:

```bash
neksus-jobspec spec migrate jobspecs/backend-engineer.jobspec.yaml
neksus-jobspec spec migrate jobspecs/backend-engineer.jobspec.yaml --json
```

## `render`

Purpose: Batch render all `*.jobspec.yaml` in configured project `spec_directory`.

Syntax:

```bash
neksus-jobspec render [--all] [--format FORMAT] [--theme THEME] [--css PATH] [--no-css] [--profile NAME] [--clean] [--json]
```

Options:

- `--all`: Alias/no-op for clarity.
- `--format`: `markdown`, `html`, `json`.
- `--theme`: Built-in render theme.
- `--css`: Append custom CSS (HTML only).
- `--no-css`: Disable embedded CSS (HTML only).
- `--profile`: Render profile name from config.
- `--clean`: Remove output directory before render.
- `--json`: Emit machine-readable JSON.

Examples:

```bash
neksus-jobspec render --format markdown
neksus-jobspec render --format html --theme modern --clean
neksus-jobspec render --profile website --json
```

## `check`

Purpose: Run project-level checks.

Syntax:

```bash
neksus-jobspec check [--strict] [--format human|github] [--json]
```

Options:

- `--strict`: Treat warnings as failures.
- `--format`: Output format (`human` or `github`).
- `--json`: Emit machine-readable JSON.

Examples:

```bash
neksus-jobspec check
neksus-jobspec check --strict
neksus-jobspec check --format github
```

JSON notes: `--json` and `--format github` are mutually exclusive.

## `themes`

Purpose: List built-in themes.

Syntax:

```bash
neksus-jobspec themes [--json]
```

Options:

- `--json`: Emit machine-readable JSON.

Examples:

```bash
neksus-jobspec themes
neksus-jobspec themes --json
```

## `themes show`

Purpose: Show metadata for one built-in theme.

Syntax:

```bash
neksus-jobspec themes show NAME [--json]
```

Options:

- `--json`: Emit machine-readable JSON.

Examples:

```bash
neksus-jobspec themes show modern
neksus-jobspec themes show default --json
```

## `config get` and `config set`

Purpose: Read and update project config values.

Syntax:

```bash
neksus-jobspec config get [KEY] [--json]
neksus-jobspec config set KEY VALUE [--json]
```

Options:

- `--json`: Emit machine-readable JSON.

Examples:

```bash
neksus-jobspec config get
neksus-jobspec config get default_format
neksus-jobspec config set strict_validation true
```
