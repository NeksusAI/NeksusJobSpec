# LLM Usage

Use this guide when asking assistants to generate or revise JobSpecs.

## Required fields

- `schema_version`
- `id`
- `page`
- `job`
- `components`

Optional:
- `campaign`
- `rendering`

## Recommended validation flow

```bash
neksus-jobspec spec validate job.jobspec.yaml
neksus-jobspec spec lint job.jobspec.yaml
neksus-jobspec spec status job.jobspec.yaml
```

## Rendering and preview

```bash
neksus-jobspec spec preview job.jobspec.yaml --no-open
neksus-jobspec spec render job.jobspec.yaml --format web --output dist/job.html
neksus-jobspec spec render job.jobspec.yaml --format json-ld --output dist/job.jsonld
```

## Export/feed commands

```bash
neksus-jobspec spec export job.jobspec.yaml --target generic-json --out dist/job.json
neksus-jobspec spec export job.jobspec.yaml --target generic-xml --out dist/job.xml
neksus-jobspec spec export job.jobspec.yaml --target linkedin-ready-json --out dist/job-linkedin.json
neksus-jobspec feed export "examples/*.jobspec.yaml" --target jobs-json --out dist/jobs.json
neksus-jobspec feed sitemap "examples/*.jobspec.yaml" --base-url https://company.dk/jobs --out dist/sitemap.xml
```

## Boundary reminders

Do not invent application forms, candidate storage, CV upload/parsing, payments, hosted API flows, or direct LinkedIn posting.
