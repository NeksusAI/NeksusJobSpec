"""Validation result normalization and warning generation."""

from __future__ import annotations

from pydantic import ValidationError

from neksus_jobspec.jobspec.models import JobSpec
from neksus_jobspec.results import ValidationIssue, ValidationResult


def _looks_like_legacy_schema(data: dict) -> bool:
    legacy_markers = {"title", "summary", "responsibilities", "requirements"}
    has_legacy = any(key in data for key in legacy_markers)
    has_components_model = "job" in data or "components" in data
    return has_legacy and not has_components_model


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


def collect_warnings(spec: JobSpec) -> list[ValidationIssue]:
    return [ValidationIssue(**warning) for warning in spec.validation_warnings()]


def validate_spec_data(data: dict) -> ValidationResult:
    if _looks_like_legacy_schema(data):
        return ValidationResult(
            valid=False,
            errors=[
                ValidationIssue(
                    path="root",
                    code="legacy_schema_removed",
                    message="Legacy schema removed in 0.2.x; use component schema or migrate.",
                )
            ],
            warnings=[],
        )
    try:
        spec = JobSpec.model_validate(data)
    except ValidationError as exc:
        return ValidationResult(valid=False, errors=pydantic_errors_to_issues(exc), warnings=[])
    warnings = collect_warnings(spec)
    return ValidationResult(valid=True, errors=[], warnings=warnings)


def validate_spec_model(spec: JobSpec) -> ValidationResult:
    return ValidationResult(valid=True, errors=[], warnings=collect_warnings(spec))
