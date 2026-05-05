# LLM Usage

Use this guide when asking assistants to generate or repair Neksus JobSpec files.

## Required top-level fields

- `schema_version`
- `id`
- `page`
- `job`
- `components`

Optional:

- `campaign`
- `rendering`

## Recommended field order

1. `schema_version`
2. `id`
3. `page`
4. `job`
5. `campaign` (optional)
6. `components`
7. `rendering` (optional)

## Campaign metadata

```yaml
campaign:
  starts_at: 2026-05-04
  expires_at: 2026-07-03
  status: active
```

Allowed status values:

- `draft`
- `active`
- `expired`
- `closed`

## Apply destination metadata

Use only apply destination metadata, not application forms.

```yaml
job:
  apply:
    method: external_url
    url: https://example.com/apply/job-id
```

Supported methods:

- `email` (requires `email`)
- `external_url` (requires `url`)
- `ats_url` (requires `url`)
- `custom` (requires `url`)
- `agent_ready` (requires `url` and `job_reference`)

## Unsupported fields (do not invent)

- `application_form`
- CV upload fields
- candidate profile fields
- payment fields
- hosted backend/API fields

## Validate and render

```bash
neksus-jobspec spec validate job.jobspec.yaml
neksus-jobspec spec render job.jobspec.yaml --format web
neksus-jobspec spec render job.jobspec.yaml --format json-ld
```

## Export and feeds

```bash
neksus-jobspec spec export job.jobspec.yaml --target generic-json --out dist/job.json
neksus-jobspec spec export job.jobspec.yaml --target generic-xml --out dist/job.xml
neksus-jobspec spec export job.jobspec.yaml --target linkedin-ready-json --out dist/linkedin-job.json
neksus-jobspec feed export "examples/*.jobspec.yaml" --target jobs-json --out dist/jobs.json
neksus-jobspec feed sitemap "examples/*.jobspec.yaml" --base-url https://company.dk/jobs --out dist/sitemap.xml
```

## Example prompts

- "Create a Danish service-role JobSpec."
- "Convert this job ad into NeksusJobSpec YAML."
- "Add campaign metadata to this JobSpec."
- "Validate this JobSpec and explain likely errors."
- "Generate a LinkedIn-ready export."
