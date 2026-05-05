# Exports

Neksus JobSpec v0.3.0 adds deterministic machine-readable exports for single jobs, multi-job feeds, and sitemaps.

LinkedIn-ready JSON is a structured export profile intended to help prepare job data for external platforms. It is not a LinkedIn API client and does not post jobs to LinkedIn.

## Single-job exports

```bash
neksus-jobspec spec export job.yaml --target generic-json --out dist/job.json
neksus-jobspec spec export job.yaml --target generic-xml --out dist/job.xml
neksus-jobspec spec export job.yaml --target linkedin-ready-json --out dist/linkedin-job.json
```

Targets:

- `generic-json`
- `generic-xml`
- `linkedin-ready-json`

## Multi-job feeds

```bash
neksus-jobspec feed export "examples/*.jobspec.yaml" --target jobs-json --out dist/jobs.json
neksus-jobspec feed export "examples/*.jobspec.yaml" --target jobs-xml --out dist/jobs.xml
```

Targets:

- `jobs-json`
- `jobs-xml`

Feed ordering is deterministic (sorted by job ID).

## Sitemap generation

```bash
neksus-jobspec feed sitemap "examples/*.jobspec.yaml" --base-url https://company.dk/jobs --out dist/sitemap.xml
```

- URLs are built from `base-url` plus JobSpec `id`.
- `lastmod` is mapped from `campaign.starts_at` when present.
- Optional filter:

```bash
neksus-jobspec feed sitemap "examples/*.jobspec.yaml" --base-url https://company.dk/jobs --out dist/sitemap.xml --exclude-closed
```
