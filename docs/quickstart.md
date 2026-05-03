# Quickstart

## 1. Initialize a project

```bash
neksus-jobspec init
```

This creates `.neksus/config.yaml`, `jobspecs/`, and `dist/`.

## 2. Create a JobSpec

```bash
neksus-jobspec spec new backend-engineer
```

## 3. Validate

```bash
neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml
```

Use strict mode to fail on warnings:

```bash
neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml --strict
```

## 4. Render

```bash
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format web --output dist/backend-engineer.html
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format json-ld --output dist/backend-engineer.json
```

## 5. Project checks

```bash
neksus-jobspec check
neksus-jobspec check --format github
neksus-jobspec check --strict
```

## 6. Batch render

```bash
neksus-jobspec render --format web
neksus-jobspec render --format web --theme modern
```

For all commands and options, see [CLI Reference](cli-reference.md).
