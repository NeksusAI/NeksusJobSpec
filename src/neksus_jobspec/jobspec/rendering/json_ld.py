"""JSON-LD renderer for schema.org JobPosting."""

from __future__ import annotations

from datetime import date

from neksus_jobspec.jobspec.rendering.normalize import normalize_jobspec_for_render
from neksus_jobspec.output import to_json


def _to_iso_date(value: str | None) -> str | None:
    if not value:
        return None
    raw = value.strip()
    if not raw:
        return None
    if len(raw) == 10 and raw[4] == "-" and raw[7] == "-":
        return raw
    if len(raw) == 10 and raw[2] == "-" and raw[5] == "-":
        day, month, year = raw.split("-")
        if len(year) == 4:
            return f"{year}-{month}-{day}"
    return raw


def render_json_ld(spec) -> str:
    """Render schema.org JobPosting JSON-LD from validated component model."""
    normalized = normalize_jobspec_for_render(spec)

    job_type = None
    region = None
    location = None
    deadline = None
    start_date = None
    reference_number = None
    company_name = None
    company_url = None
    contact_email = None
    contact_name = None
    responsibilities: list[str] = []
    qualifications: list[str] = []
    benefits: list[str] = []

    for component in normalized.components:
        if component.type == "meta_panel":
            for fact in component.facts:
                label = fact.label.strip().lower()
                value = fact.value.strip()
                if "jobtype" in label or "employment" in label:
                    job_type = value
                elif "region" in label:
                    region = value
                elif "arbejdssted" in label or "workplace" in label or "location" in label:
                    location = value
                elif "ansøgningsfrist" in label or "deadline" in label:
                    deadline = _to_iso_date(value)
                elif "tiltrædelse" in label or "start" in label:
                    start_date = _to_iso_date(value)
                elif "referencenummer" in label or "reference" in label:
                    reference_number = value
            contact_email = component.contact_email or contact_email
            contact_name = component.contact_name or contact_name

        elif component.type == "header_brand":
            company_name = component.brand_name or company_name
            company_url = component.brand_url or company_url
        elif component.type == "footer_brand":
            company_name = component.brand_name or company_name
            if component.links:
                company_url = component.links[0].url or company_url
        elif component.type == "company_profile":
            company_name = component.title or company_name
        elif component.type == "list":
            title = (component.title or "").strip().lower()
            if "opgave" in title or "responsib" in title:
                responsibilities.extend(component.items)
            elif "krav" in title or "qualif" in title:
                qualifications.extend(component.items)
        elif component.type == "benefits":
            for benefit in component.items:
                if isinstance(benefit, str):
                    benefits.append(benefit)
                else:
                    text = benefit.get("text")
                    if text:
                        benefits.append(text)

    campaign_start = (
        normalized.campaign_starts_at.isoformat() if normalized.campaign_starts_at else None
    )
    campaign_expiry = (
        normalized.campaign_expires_at.isoformat() if normalized.campaign_expires_at else None
    )

    payload = {
        "@context": "https://schema.org",
        "@type": "JobPosting",
        "identifier": {
            "@type": "PropertyValue",
            "name": reference_number or spec.id,
            "value": spec.id,
        },
        "title": normalized.title,
        "description": normalized.intro or normalized.title,
        "datePosted": campaign_start or date.today().isoformat(),
        "validThrough": campaign_expiry or deadline,
        "employmentType": job_type,
        "hiringOrganization": {
            "@type": "Organization",
            "name": company_name or "Hiring Organization",
            "sameAs": company_url,
        },
        "jobLocation": {
            "@type": "Place",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": location,
                "addressRegion": region,
            },
        },
        "applicationContact": {
            "@type": "ContactPoint",
            "name": contact_name,
            "email": contact_email,
        },
        "url": normalized.apply_url,
        "directApply": bool(normalized.apply_url),
        "jobStartDate": start_date,
        "responsibilities": "\n".join(responsibilities) if responsibilities else None,
        "qualifications": "\n".join(qualifications) if qualifications else None,
        "jobBenefits": "\n".join(benefits) if benefits else None,
    }

    clean_payload = {
        key: value
        for key, value in payload.items()
        if value not in (None, "", [])
        and (
            not isinstance(value, dict)
            or any(inner not in (None, "", []) for inner in value.values())
        )
    }
    return to_json(clean_payload)
