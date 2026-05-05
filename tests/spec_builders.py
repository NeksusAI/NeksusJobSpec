from __future__ import annotations

from pathlib import Path


def write_export_spec(path: Path, job_id: str = "export-role", status: str = "active") -> None:
    path.write_text(
        f"""schema_version: 1
id: {job_id}
page:
  layout: job_detail
job:
  title: {job_id}
  apply:
    method: external_url
    url: https://example.com/apply/{job_id}
campaign:
  starts_at: 2026-05-04
  expires_at: 2026-07-03
  status: {status}
components:
  - type: meta_chips
    id: chips
    items:
      - label: Location
        value: Copenhagen, Denmark
        icon: location_on
      - label: Employment
        value: FULL_TIME
        icon: work
  - type: list
    id: requirements
    items:
      - One
""",
        encoding="utf-8",
    )
