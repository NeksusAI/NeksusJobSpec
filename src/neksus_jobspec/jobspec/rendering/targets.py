"""Typed rendering targets and serializers for JSON-LD and feed outputs."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from pydantic import BaseModel, ConfigDict, Field

from neksus_jobspec.jobspec.exports import normalized_export_payload
from neksus_jobspec.jobspec.models import JobSpec
from neksus_jobspec.jobspec.rendering.normalize import normalize_jobspec_for_render
from neksus_jobspec.output import to_json


class StrictOutputModel(BaseModel):
    """Base output model that rejects unknown fields."""

    model_config = ConfigDict(extra="forbid")


class JsonLdPropertyValue(StrictOutputModel):
    type_name: str = Field(default="PropertyValue", alias="@type")
    name: str
    value: str


class JsonLdOrganization(StrictOutputModel):
    type_name: str = Field(default="Organization", alias="@type")
    name: str
    sameAs: str | None = None


class JsonLdPostalAddress(StrictOutputModel):
    type_name: str = Field(default="PostalAddress", alias="@type")
    streetAddress: str | None = None
    addressRegion: str | None = None


class JsonLdPlace(StrictOutputModel):
    type_name: str = Field(default="Place", alias="@type")
    address: JsonLdPostalAddress


class JsonLdContactPoint(StrictOutputModel):
    type_name: str = Field(default="ContactPoint", alias="@type")
    name: str | None = None
    email: str | None = None


class JsonLdJobPosting(StrictOutputModel):
    context: str = Field(default="https://schema.org", alias="@context")
    type_name: str = Field(default="JobPosting", alias="@type")
    identifier: JsonLdPropertyValue
    title: str
    description: str
    datePosted: str
    validThrough: str | None = None
    employmentType: str | None = None
    hiringOrganization: JsonLdOrganization
    jobLocation: JsonLdPlace
    applicationContact: JsonLdContactPoint
    url: str | None = None
    directApply: bool
    jobStartDate: str | None = None
    responsibilities: str | None = None
    qualifications: str | None = None
    jobBenefits: str | None = None

    def as_payload(self) -> dict[str, Any]:
        """Return compact JSON-safe payload with empty values removed."""
        raw = self.model_dump(by_alias=True, mode="json", exclude_none=True)
        compact: dict[str, Any] = {}
        for key, value in raw.items():
            if value in ("", [], {}):
                continue
            if isinstance(value, dict):
                nested = {k: v for k, v in value.items() if v not in ("", [], {}, None)}
                if nested:
                    compact[key] = nested
                continue
            compact[key] = value
        return compact


class FeedApply(StrictOutputModel):
    method: str | None = None
    url: str | None = None
    email: str | None = None


class FeedCampaign(StrictOutputModel):
    status: str | None = None
    starts_at: str | None = None
    expires_at: str | None = None


class FeedCompany(StrictOutputModel):
    name: str | None = None


class FeedJobEntry(StrictOutputModel):
    id: str
    title: str
    location: str | None = None
    company: FeedCompany | None = None
    apply: FeedApply | None = None
    campaign: FeedCampaign | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


class JobsJsonFeed(StrictOutputModel):
    generated_by: str = "neksus-jobspec"
    feed_type: str = "jobs-json"
    jobs: list[FeedJobEntry]


class JobsXmlEntry(StrictOutputModel):
    id: str
    title: str
    company_name: str | None = None
    location: str | None = None
    apply: FeedApply | None = None
    campaign: FeedCampaign | None = None


class JobsXmlFeed(StrictOutputModel):
    generated_by: str = "neksus-jobspec"
    jobs: list[JobsXmlEntry]


class SitemapUrlEntry(StrictOutputModel):
    loc: str
    lastmod: str | None = None


class SitemapDocument(StrictOutputModel):
    urls: list[SitemapUrlEntry]


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


def _sorted_specs(specs: list[JobSpec]) -> list[JobSpec]:
    return sorted(specs, key=lambda item: item.id)


def build_json_ld_target(spec: JobSpec) -> JsonLdJobPosting:
    """Build typed JSON-LD target model from validated JobSpec."""
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

    return JsonLdJobPosting(
        identifier=JsonLdPropertyValue(name=reference_number or spec.id, value=spec.id),
        title=normalized.title,
        description=normalized.intro or normalized.title,
        datePosted=campaign_start or date.today().isoformat(),
        validThrough=campaign_expiry or deadline,
        employmentType=job_type,
        hiringOrganization=JsonLdOrganization(
            name=company_name or "Hiring Organization", sameAs=company_url
        ),
        jobLocation=JsonLdPlace(
            address=JsonLdPostalAddress(streetAddress=location, addressRegion=region)
        ),
        applicationContact=JsonLdContactPoint(name=contact_name, email=contact_email),
        url=normalized.apply_url,
        directApply=bool(normalized.apply_url),
        jobStartDate=start_date,
        responsibilities="\n".join(responsibilities) if responsibilities else None,
        qualifications="\n".join(qualifications) if qualifications else None,
        jobBenefits="\n".join(benefits) if benefits else None,
    )


def render_json_ld(spec: JobSpec) -> str:
    """Render schema.org JobPosting JSON-LD from validated component model."""
    target = build_json_ld_target(spec)
    return to_json(target.as_payload())


def build_jobs_json_feed_target(specs: list[JobSpec]) -> JobsJsonFeed:
    """Build typed jobs-json feed target from JobSpecs."""
    jobs: list[FeedJobEntry] = []
    for spec in _sorted_specs(specs):
        payload = normalized_export_payload(spec)
        apply = payload.get("apply") if isinstance(payload.get("apply"), dict) else {}
        campaign = payload.get("campaign") if isinstance(payload.get("campaign"), dict) else {}
        company = payload.get("company") if isinstance(payload.get("company"), dict) else {}
        jobs.append(
            FeedJobEntry(
                id=str(payload.get("id") or spec.id),
                title=str(payload.get("title") or spec.job.title),
                location=(str(payload.get("location")) if payload.get("location") else None),
                company=FeedCompany(name=str(company.get("name")) if company.get("name") else None),
                apply=FeedApply(
                    method=str(apply.get("method")) if apply.get("method") else None,
                    url=str(apply.get("url")) if apply.get("url") else None,
                    email=str(apply.get("email")) if apply.get("email") else None,
                ),
                campaign=FeedCampaign(
                    status=str(campaign.get("status")) if campaign.get("status") else None,
                    starts_at=str(campaign.get("starts_at")) if campaign.get("starts_at") else None,
                    expires_at=str(campaign.get("expires_at"))
                    if campaign.get("expires_at")
                    else None,
                ),
                raw=payload,
            )
        )
    return JobsJsonFeed(jobs=jobs)


def render_jobs_json_feed(specs: list[JobSpec]) -> str:
    """Render deterministic jobs-json feed."""
    feed = build_jobs_json_feed_target(specs)
    payload = {
        "generated_by": feed.generated_by,
        "feed_type": feed.feed_type,
        "jobs": [entry.raw for entry in feed.jobs],
    }
    return to_json(payload)


def build_jobs_xml_feed_target(specs: list[JobSpec]) -> JobsXmlFeed:
    """Build typed jobs-xml feed target from JobSpecs."""
    jobs: list[JobsXmlEntry] = []
    for spec in _sorted_specs(specs):
        payload = normalized_export_payload(spec)
        company = payload.get("company") if isinstance(payload.get("company"), dict) else {}
        apply = payload.get("apply") if isinstance(payload.get("apply"), dict) else {}
        campaign = payload.get("campaign") if isinstance(payload.get("campaign"), dict) else {}
        jobs.append(
            JobsXmlEntry(
                id=str(payload.get("id") or spec.id),
                title=str(payload.get("title") or spec.job.title),
                company_name=str(company.get("name")) if company.get("name") else None,
                location=str(payload.get("location")) if payload.get("location") else None,
                apply=FeedApply(
                    method=str(apply.get("method")) if apply.get("method") else None,
                    url=str(apply.get("url")) if apply.get("url") else None,
                    email=str(apply.get("email")) if apply.get("email") else None,
                ),
                campaign=FeedCampaign(
                    status=str(campaign.get("status")) if campaign.get("status") else None,
                    starts_at=str(campaign.get("starts_at")) if campaign.get("starts_at") else None,
                    expires_at=str(campaign.get("expires_at"))
                    if campaign.get("expires_at")
                    else None,
                ),
            )
        )
    return JobsXmlFeed(jobs=jobs)


def render_jobs_xml_feed(specs: list[JobSpec]) -> str:
    """Render deterministic jobs-xml feed."""
    feed = build_jobs_xml_feed_target(specs)
    root = ET.Element("jobs", {"generatedBy": feed.generated_by})
    for entry in feed.jobs:
        job = ET.SubElement(root, "job")
        ET.SubElement(job, "id").text = entry.id
        ET.SubElement(job, "title").text = entry.title
        ET.SubElement(job, "companyName").text = entry.company_name or ""
        ET.SubElement(job, "location").text = entry.location or ""
        if entry.apply:
            apply_node = ET.SubElement(job, "apply")
            ET.SubElement(apply_node, "method").text = entry.apply.method or ""
            ET.SubElement(apply_node, "url").text = entry.apply.url or ""
            ET.SubElement(apply_node, "email").text = entry.apply.email or ""
        if entry.campaign:
            campaign_node = ET.SubElement(job, "campaign")
            ET.SubElement(campaign_node, "status").text = entry.campaign.status or ""
            ET.SubElement(campaign_node, "startsAt").text = entry.campaign.starts_at or ""
            ET.SubElement(campaign_node, "expiresAt").text = entry.campaign.expires_at or ""
    return ET.tostring(root, encoding="unicode")


def build_sitemap_target(
    specs: list[JobSpec],
    base_url: str,
    *,
    exclude_closed: bool = False,
) -> SitemapDocument:
    """Build typed sitemap target from JobSpecs."""
    urls: list[SitemapUrlEntry] = []
    for spec in _sorted_specs(specs):
        status = spec.campaign.status if spec.campaign else None
        if exclude_closed and status in {"closed", "expired"}:
            continue
        loc = base_url.rstrip("/") + "/" + spec.id
        lastmod = (
            spec.campaign.starts_at.isoformat()
            if spec.campaign and spec.campaign.starts_at
            else None
        )
        urls.append(SitemapUrlEntry(loc=loc, lastmod=lastmod))
    return SitemapDocument(urls=urls)


def render_sitemap(specs: list[JobSpec], base_url: str, *, exclude_closed: bool = False) -> str:
    """Render sitemap XML document."""
    target = build_sitemap_target(specs, base_url, exclude_closed=exclude_closed)
    root = ET.Element("urlset", {"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"})
    for entry in target.urls:
        url = ET.SubElement(root, "url")
        ET.SubElement(url, "loc").text = entry.loc
        if entry.lastmod:
            ET.SubElement(url, "lastmod").text = entry.lastmod
    return ET.tostring(root, encoding="unicode")


def expand_input_paths(inputs: list[str]) -> list[Path]:
    """Expand file, directory, and glob inputs into unique file paths."""
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
