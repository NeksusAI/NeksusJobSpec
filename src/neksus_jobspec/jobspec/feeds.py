"""Feed and sitemap generation helpers."""

from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

from neksus_jobspec.jobspec.exports import normalized_export_payload
from neksus_jobspec.jobspec.models import JobSpec
from neksus_jobspec.output import to_json


def sorted_specs(specs: list[JobSpec]) -> list[JobSpec]:
    return sorted(specs, key=lambda item: item.id)


def render_jobs_json_feed(specs: list[JobSpec]) -> str:
    ordered = sorted_specs(specs)
    payload = {
        "generated_by": "neksus-jobspec",
        "feed_type": "jobs-json",
        "jobs": [normalized_export_payload(spec) for spec in ordered],
    }
    return to_json(payload)


def render_jobs_xml_feed(specs: list[JobSpec]) -> str:
    ordered = sorted_specs(specs)
    root = ET.Element("jobs", {"generatedBy": "neksus-jobspec"})
    for spec in ordered:
        payload = normalized_export_payload(spec)
        job = ET.SubElement(root, "job")
        ET.SubElement(job, "id").text = str(payload["id"])
        ET.SubElement(job, "title").text = str(payload["title"])
        company = payload.get("company")
        if isinstance(company, dict):
            ET.SubElement(job, "companyName").text = str(company.get("name") or "")
        ET.SubElement(job, "location").text = str(payload.get("location") or "")
        apply = payload.get("apply")
        if isinstance(apply, dict):
            apply_node = ET.SubElement(job, "apply")
            ET.SubElement(apply_node, "method").text = str(apply.get("method") or "")
            ET.SubElement(apply_node, "url").text = str(apply.get("url") or "")
            ET.SubElement(apply_node, "email").text = str(apply.get("email") or "")
        campaign = payload.get("campaign")
        if isinstance(campaign, dict):
            campaign_node = ET.SubElement(job, "campaign")
            ET.SubElement(campaign_node, "status").text = str(campaign.get("status") or "")
            ET.SubElement(campaign_node, "startsAt").text = str(campaign.get("starts_at") or "")
            ET.SubElement(campaign_node, "expiresAt").text = str(campaign.get("expires_at") or "")
    return ET.tostring(root, encoding="unicode")


def render_sitemap(specs: list[JobSpec], base_url: str, *, exclude_closed: bool = False) -> str:
    ordered = sorted_specs(specs)
    root = ET.Element("urlset", {"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"})
    for spec in ordered:
        status = spec.campaign.status if spec.campaign else None
        if exclude_closed and status in {"closed", "expired"}:
            continue
        url = ET.SubElement(root, "url")
        slug = spec.id
        loc = base_url.rstrip("/") + "/" + slug
        ET.SubElement(url, "loc").text = loc
        if spec.campaign and spec.campaign.starts_at:
            ET.SubElement(url, "lastmod").text = spec.campaign.starts_at.isoformat()
    return ET.tostring(root, encoding="unicode")


def expand_input_paths(inputs: list[str]) -> list[Path]:
    resolved: list[Path] = []
    for item in inputs:
        path = Path(item)
        if path.is_dir():
            resolved.extend(sorted(path.glob("*.jobspec.yaml")))
            continue
        matches = sorted(Path().glob(item))
        if matches:
            resolved.extend(match for match in matches if match.is_file())
            continue
        if path.exists() and path.is_file():
            resolved.append(path)
    unique: dict[str, Path] = {}
    for entry in resolved:
        unique[str(entry.resolve())] = entry
    return list(unique.values())
