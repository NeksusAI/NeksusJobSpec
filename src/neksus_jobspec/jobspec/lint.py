"""Advisory quality lint checks for validated JobSpecs."""

from __future__ import annotations

from datetime import date

from neksus_jobspec.jobspec.models import JobSpec
from neksus_jobspec.results import ValidationIssue


def lint_jobspec(spec: JobSpec, today: date | None = None) -> list[ValidationIssue]:
    """Return non-failing quality warnings for a validated JobSpec."""
    warnings = [ValidationIssue(**item) for item in spec.validation_warnings()]

    apply = spec.job.apply
    if apply is None:
        warnings.append(
            ValidationIssue(
                path="job.apply",
                code="missing_apply",
                message="Apply destination is missing.",
            )
        )
    elif apply.url and not apply.url.lower().startswith("https://"):
        warnings.append(
            ValidationIssue(
                path="job.apply.url",
                code="apply_url_not_https",
                message="Apply URL should use HTTPS.",
            )
        )

    if spec.job.intro and len(spec.job.intro.strip()) < 60:
        warnings.append(
            ValidationIssue(
                path="job.intro",
                code="intro_too_short",
                message="Job intro is very short; consider adding more context.",
            )
        )

    has_salary = any(
        component.type == "meta_chips"
        and any(
            (item.semantic == "salary") or ("salary" in item.label.lower())
            for item in component.items
        )
        for component in spec.components
    )
    if not has_salary:
        warnings.append(
            ValidationIssue(
                path="components",
                code="missing_salary",
                message="Salary/range metadata is missing.",
            )
        )

    has_location = any(
        component.type == "meta_chips"
        and any(
            (item.semantic == "location") or ("location" in item.label.lower())
            for item in component.items
        )
        for component in spec.components
    )

    has_onsite_or_hybrid = any(
        component.type == "meta_chips"
        and any(
            "onsite" in item.value.lower() or "hybrid" in item.value.lower()
            for item in component.items
            if "workplace" in item.label.lower() or "mode" in item.label.lower()
        )
        for component in spec.components
    )

    if has_onsite_or_hybrid and not has_location:
        warnings.append(
            ValidationIssue(
                path="components",
                code="missing_structured_location",
                message="Onsite/hybrid role is missing structured location metadata.",
            )
        )

    status = spec.campaign.status if spec.campaign else None
    days_remaining = spec.days_remaining(today=today)
    if days_remaining is not None and days_remaining < 0 and status == "active":
        warnings.append(
            ValidationIssue(
                path="campaign.status",
                code="campaign_status_mismatch",
                message="Campaign is expired by date but status is still active.",
            )
        )

    if spec.campaign is None:
        warnings.append(
            ValidationIssue(
                path="campaign",
                code="missing_campaign_metadata",
                message="Campaign metadata is missing.",
            )
        )

    has_json_ld_company = any(component.type == "header_brand" for component in spec.components)
    if not has_json_ld_company:
        warnings.append(
            ValidationIssue(
                path="components",
                code="missing_company_profile_hint",
                message="Company branding metadata is missing (header_brand recommended).",
            )
        )

    return warnings
