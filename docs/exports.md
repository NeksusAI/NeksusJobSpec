# Exports, Feeds, and Sitemap

Neksus JobSpec provides deterministic machine-readable outputs for downstream systems.

## When to use each command

- `spec export`: one JobSpec -> one output file.
- `feed export`: multiple JobSpecs -> one aggregate feed file.
- `feed sitemap`: multiple JobSpecs -> sitemap XML for discoverability.

## Single-job exports

```bash
neksus-jobspec spec export examples/startup-engineer.jobspec.yaml --target generic-json --out dist/job.json
neksus-jobspec spec export examples/startup-engineer.jobspec.yaml --target generic-xml --out dist/job.xml
neksus-jobspec spec export examples/startup-engineer.jobspec.yaml --target linkedin-ready-json --out dist/job-linkedin.json
```

Targets:
- `generic-json`
- `generic-xml`
- `linkedin-ready-json`

Downloadable examples:
- [`generic-export.sample.json`](examples/generic-export.sample.json)
- [`generic-export.sample.xml`](examples/generic-export.sample.xml)
- [`linkedin-ready.sample.json`](examples/linkedin-ready.sample.json)

### Generic JSON sample

```json
{
  "id": "startup-engineer",
  "title": "Startup Engineer"
}
```

### LinkedIn-ready JSON sample

```json
{
  "externalJobPostingId": "startup-engineer",
  "title": "Startup Engineer"
}
```

`linkedin-ready-json` is a data shape only, not a posting integration.

## Multi-job feeds

```bash
neksus-jobspec feed export "examples/*.jobspec.yaml" --target jobs-json --out dist/jobs.json
neksus-jobspec feed export "examples/*.jobspec.yaml" --target jobs-xml --out dist/jobs.xml
```

Feed ordering is deterministic (sorted by JobSpec `id`).

Downloadable examples:
- [`feed-jobs.sample.json`](examples/feed-jobs.sample.json)
- [`feed-jobs.sample.xml`](examples/feed-jobs.sample.xml)

## Sitemap

```bash
neksus-jobspec feed sitemap "examples/*.jobspec.yaml" --base-url https://company.dk/jobs --out dist/sitemap.xml
neksus-jobspec feed sitemap "examples/*.jobspec.yaml" --base-url https://company.dk/jobs --out dist/sitemap.xml --exclude-closed
```

Behavior:
- URL path uses JobSpec `id`.
- `lastmod` maps from `campaign.starts_at` when present.
- `--exclude-closed` drops `closed` and `expired` campaigns.

Downloadable example:
- [`sitemap.sample.xml`](examples/sitemap.sample.xml)

## Common pitfalls

- Export commands use `--out` (not `--output`).
- Validate specs before feed/sitemap commands.
- Use HTTPS apply URLs for best compatibility with external consumers.
