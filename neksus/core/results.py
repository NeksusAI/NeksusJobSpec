"""Shared result models for validation and project checks.

These models are intentionally stable because they are used by CLI JSON
output and can become part of the public package contract.
"""

from __future__ import annotations

from pydantic import BaseModel


class ValidationIssue(BaseModel):
    """Single validation issue with stable path/code/message fields."""

    path: str
    code: str
    message: str


class ValidationResult(BaseModel):
    """Result of validating one JobSpec file."""

    valid: bool
    errors: list[ValidationIssue]
    warnings: list[ValidationIssue]


class ProjectCheck(BaseModel):
    """Single project-level check status."""

    name: str
    ok: bool
    message: str


class ProjectCheckResult(BaseModel):
    """Aggregate result for all project-level checks."""

    ok: bool
    checks: list[ProjectCheck]
    errors: list[ValidationIssue]
    warnings: list[ValidationIssue]
