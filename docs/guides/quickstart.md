# Quickstart

## 1. Initialize a project

```bash
neksus-jobspec init
```

## 2. Run environment health checks

```bash
neksus-jobspec doctor
```

## 3. Create and validate a JobSpec

```bash
neksus-jobspec spec new backend-engineer
neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml
```

## 4. Run quality lint and status checks

```bash
neksus-jobspec spec lint jobspecs/backend-engineer.jobspec.yaml
neksus-jobspec spec status jobspecs/backend-engineer.jobspec.yaml
```

## 5. Preview and render

```bash
neksus-jobspec spec preview jobspecs/backend-engineer.jobspec.yaml --no-open
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format web --output dist/backend-engineer.html
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format json-ld --output dist/backend-engineer.jsonld
```

## 6. Export and feed outputs

```bash
neksus-jobspec spec export jobspecs/backend-engineer.jobspec.yaml --target generic-json --out dist/backend-engineer.json
neksus-jobspec feed export "jobspecs/*.jobspec.yaml" --target jobs-json --out dist/jobs.json
neksus-jobspec feed sitemap "jobspecs/*.jobspec.yaml" --base-url https://company.dk/jobs --out dist/sitemap.xml
```

## 7. Theme developer flow (optional)

```bash
neksus-jobspec themes list
neksus-jobspec themes init my-theme
neksus-jobspec themes validate my-theme
```
