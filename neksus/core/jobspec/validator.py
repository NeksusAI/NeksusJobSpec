"""Validation result normalization and warning generation.

This module separates hard validation errors from soft warnings and
converts third-party validation output into stable Neksus issue shapes.
"""

from __future__ import annotations

from collections import Counter

from pydantic import ValidationError

from neksus.core.jobspec.models import JobSpec
from neksus.core.results import ValidationIssue, ValidationResult


def pydantic_errors_to_issues(exc: ValidationError) -> list[ValidationIssue]:
    """Convert Pydantic ValidationError details into stable issue objects."""
    issues: list[ValidationIssue] = []
    for error in exc.errors():
        loc = ".".join(str(part) for part in error["loc"]) or "root"
        issues.append(
            ValidationIssue(
                path=loc,
                code=str(error["type"]),
                message=str(error["msg"]),
            )
        )
    return issues


def _normalized_counts(values: list[str]) -> Counter[str]:
    """Count values with normalization for duplicate-detection warnings."""
    return Counter(item.strip().lower() for item in values)


def collect_warnings(spec: JobSpec) -> list[ValidationIssue]:
    """Generate non-fatal warnings for a valid JobSpec model."""
    warnings: list[ValidationIssue] = []

    # Short title warning (non-fatal).
    if len(spec.title.strip()) < 5:
        warnings.append(
            ValidationIssue(path="title", code="short_title", message="Title is very short.")
        )

    resp_counts = _normalized_counts(spec.responsibilities)
    # Case-insensitive duplicate warnings.
    if any(count > 1 for count in resp_counts.values()):
        warnings.append(
            ValidationIssue(
                path="responsibilities",
                code="duplicate_items",
                message="Duplicate responsibilities found.",
            )
        )

    req_counts = _normalized_counts(spec.requirements)
    if any(count > 1 for count in req_counts.values()):
        warnings.append(
            ValidationIssue(
                path="requirements",
                code="duplicate_items",
                message="Duplicate requirements found.",
            )
        )

    if spec.location and spec.location.type in {"hybrid", "onsite"}:
        if not spec.location.city and not spec.location.country:
            warnings.append(
                ValidationIssue(
                    path="location",
                    code="missing_location_detail",
                    message="Hybrid or onsite role should include city or country.",
                )
            )

    return warnings


def validate_spec_data(data: dict) -> ValidationResult:
    """Validate raw spec data dictionary into errors/warnings."""
    try:
        spec = JobSpec.model_validate(data)
    except ValidationError as exc:
        return ValidationResult(valid=False, errors=pydantic_errors_to_issues(exc), warnings=[])
    warnings = collect_warnings(spec)
    return ValidationResult(valid=True, errors=[], warnings=warnings)


def validate_spec_model(spec: JobSpec) -> ValidationResult:
    """Validate warning-level rules for an already validated model."""
    return ValidationResult(valid=True, errors=[], warnings=collect_warnings(spec))
