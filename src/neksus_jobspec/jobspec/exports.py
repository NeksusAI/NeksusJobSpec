"""Machine-readable export helpers for JobSpecs."""

from __future__ import annotations

from xml.etree import ElementTree as ET

from neksus_jobspec.jobspec.models import JobSpec
from neksus_jobspec.jobspec.rendering.normalize import normalize_apply
from neksus_jobspec.output import to_json


def _description(spec: JobSpec) -> str:
    if spec.job.intro:
        return spec.job.intro
    for component in spec.components:
        if component.type == "rich_text" and component.body.strip():
            return component.body
    return spec.job.title


def _company_name(spec: JobSpec) -> str | None:
    for component in spec.components:
        if component.type == "header_brand":
            return component.brand_name
    return None


def _location(spec: JobSpec) -> str | None:
    for component in spec.components:
        if component.type == "meta_chips":
            for item in component.items:
                if "location" in item.label.lower():
                    return item.value
    return None


def _employment(spec: JobSpec) -> str | None:
    for component in spec.components:
        if component.type == "meta_chips":
            for item in component.items:
                if "employment" in item.label.lower() or "type" in item.label.lower():
                    return item.value
    return None


def normalized_export_payload(spec: JobSpec) -> dict[str, object]:
    apply_label, apply_url, apply_method = normalize_apply(spec)
    return {
        "schema_version": spec.schema_version,
        "id": spec.id,
        "page": spec.page.model_dump(mode="json"),
        "title": spec.job.title,
        "company": {"name": _company_name(spec)},
        "location": _location(spec),
        "employment": _employment(spec),
        "description": _description(spec),
        "apply": {
            "method": apply_method,
            "label": apply_label,
            "url": apply_url,
            "email": spec.job.apply.email if spec.job.apply else None,
            "job_reference": spec.job.apply.job_reference if spec.job.apply else None,
        },
        "campaign": spec.campaign.model_dump(mode="json") if spec.campaign else None,
        "components": [
            {"id": component.id, "type": component.type} for component in spec.components
        ],
    }


def render_generic_json(spec: JobSpec) -> str:
    return to_json(spec.export_payload("generic"))


def render_generic_xml(spec: JobSpec) -> str:
    payload = normalized_export_payload(spec)
    root = ET.Element("jobspec")
    ET.SubElement(root, "schemaVersion").text = str(payload["schema_version"])
    ET.SubElement(root, "id").text = str(payload["id"])
    ET.SubElement(root, "title").text = str(payload["title"])
    company = payload["company"]
    if isinstance(company, dict):
        ET.SubElement(root, "companyName").text = str(company.get("name") or "")
    ET.SubElement(root, "location").text = str(payload.get("location") or "")
    ET.SubElement(root, "employment").text = str(payload.get("employment") or "")
    ET.SubElement(root, "description").text = str(payload.get("description") or "")

    apply = payload["apply"]
    if isinstance(apply, dict):
        apply_node = ET.SubElement(root, "apply")
        ET.SubElement(apply_node, "method").text = str(apply.get("method") or "")
        ET.SubElement(apply_node, "label").text = str(apply.get("label") or "")
        ET.SubElement(apply_node, "url").text = str(apply.get("url") or "")
        ET.SubElement(apply_node, "email").text = str(apply.get("email") or "")
        ET.SubElement(apply_node, "jobReference").text = str(apply.get("job_reference") or "")

    if spec.campaign:
        campaign = ET.SubElement(root, "campaign")
        ET.SubElement(campaign, "status").text = spec.campaign.status or ""
        ET.SubElement(campaign, "startsAt").text = (
            spec.campaign.starts_at.isoformat() if spec.campaign.starts_at else ""
        )
        ET.SubElement(campaign, "expiresAt").text = (
            spec.campaign.expires_at.isoformat() if spec.campaign.expires_at else ""
        )

    return ET.tostring(root, encoding="unicode")


def render_linkedin_ready_json(spec: JobSpec) -> tuple[str, list[str]]:
    payload = spec.export_payload("generic")
    apply = payload["apply"] if isinstance(payload["apply"], dict) else {}
    company_apply_url = apply.get("url")
    warnings: list[str] = []
    if not payload.get("location"):
        warnings.append("location is missing; many job boards expect it")
    if not payload.get("employment"):
        warnings.append("employment is missing; many job boards expect it")
    if not company_apply_url:
        warnings.append("companyApplyUrl is missing; URL-based apply method is recommended")

    linkedin = spec.export_payload("linkedin-ready")
    return to_json(linkedin), warnings
