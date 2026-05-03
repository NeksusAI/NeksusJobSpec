"""Validation result normalization and warning generation."""

from __future__ import annotations

from collections import Counter

from pydantic import ValidationError

from neksus.core.jobspec.models import JobSpec, ListComponent
from neksus.core.results import ValidationIssue, ValidationResult


def pydantic_errors_to_issues(exc: ValidationError) -> list[ValidationIssue]:
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
    return Counter(item.strip().lower() for item in values)


def collect_warnings(spec: JobSpec) -> list[ValidationIssue]:
    warnings: list[ValidationIssue] = []

    if len(spec.job.title.strip()) < 5:
        warnings.append(
            ValidationIssue(path="job.title", code="short_title", message="Title is very short.")
        )

    list_components = [
        component for component in spec.components if isinstance(component, ListComponent)
    ]
    for component in list_components:
        counts = _normalized_counts(component.items)
        if any(count > 1 for count in counts.values()):
            warnings.append(
                ValidationIssue(
                    path=f"components.{component.id}",
                    code="duplicate_items",
                    message=f"Duplicate items found in list component '{component.id}'.",
                )
            )

    return warnings


def validate_spec_data(data: dict) -> ValidationResult:
    try:
        spec = JobSpec.model_validate(data)
    except ValidationError as exc:
        return ValidationResult(valid=False, errors=pydantic_errors_to_issues(exc), warnings=[])
    warnings = collect_warnings(spec)
    return ValidationResult(valid=True, errors=[], warnings=warnings)


def validate_spec_model(spec: JobSpec) -> ValidationResult:
    return ValidationResult(valid=True, errors=[], warnings=collect_warnings(spec))
