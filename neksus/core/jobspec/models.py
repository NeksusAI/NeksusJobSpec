"""Pydantic models for JobSpec data.

Defines the canonical schema for JobSpec documents.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class Location(BaseModel):
    """Location model for a job role."""

    type: Literal["remote", "hybrid", "onsite"]
    city: str | None = None
    country: str | None = None


class Employment(BaseModel):
    """Employment type model."""

    type: Literal["full-time", "part-time", "contract", "internship"]


class JobSpec(BaseModel):
    """Top-level JobSpec model."""

    schema_version: int = 1
    id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    title: str
    department: str | None = None
    level: str | None = None
    location: Location | None = None
    summary: str
    responsibilities: list[str] = Field(min_length=1)
    requirements: list[str] = Field(min_length=1)
    nice_to_have: list[str] = Field(default_factory=list)
    employment: Employment | None = None

    @field_validator("schema_version")
    @classmethod
    def validate_schema_version(cls, value: int) -> int:
        """Require current schema version."""
        if value != 1:
            raise ValueError("schema_version must be 1")
        return value

    @field_validator("title", "summary")
    @classmethod
    def validate_non_empty_text(cls, value: str) -> str:
        """Require non-empty text fields."""
        if not value.strip():
            raise ValueError("must not be empty")
        return value

    @field_validator("responsibilities", "requirements", "nice_to_have")
    @classmethod
    def validate_non_empty_items(cls, value: list[str]) -> list[str]:
        """Require list fields to contain non-empty string entries."""
        if any(not item.strip() for item in value):
            raise ValueError("must contain only non-empty strings")
        return value
