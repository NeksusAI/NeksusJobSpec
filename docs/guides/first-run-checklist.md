# First Run Checklist

Use this checklist for a clean first local setup.

## 1. Install

```bash
pip install neksus-jobspec
```

Optional MCP tools:

```bash
pip install "neksus-jobspec[mcp]"
```

## 2. Confirm CLI is healthy

```bash
neksus-jobspec --help
neksus-jobspec doctor
```

## 3. Initialize a workspace

```bash
mkdir jobspec-demo && cd jobspec-demo
neksus-jobspec init
```

## 4. Create and verify a spec

```bash
neksus-jobspec spec new backend-engineer
neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml
neksus-jobspec spec lint jobspecs/backend-engineer.jobspec.yaml
neksus-jobspec spec status jobspecs/backend-engineer.jobspec.yaml
```

## 5. Render and preview

```bash
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format web --output dist/backend-engineer.html
neksus-jobspec spec preview jobspecs/backend-engineer.jobspec.yaml --no-open
```

## 6. Export machine-readable formats

```bash
neksus-jobspec spec export jobspecs/backend-engineer.jobspec.yaml --target generic-json --out dist/backend-engineer.json
neksus-jobspec feed export "jobspecs/*.jobspec.yaml" --target jobs-json --out dist/jobs.json
neksus-jobspec feed sitemap "jobspecs/*.jobspec.yaml" --base-url https://company.dk/jobs --out dist/sitemap.xml
```

## 7. Theme developer flow (optional)

```bash
neksus-jobspec themes init my-theme
neksus-jobspec themes validate my-theme
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format web --theme ./my-theme --output dist/backend-engineer-custom.html
```
