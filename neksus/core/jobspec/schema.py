"""JSON Schema export helpers for JobSpec."""

from __future__ import annotations

from typing import Any

from neksus.core.jobspec.models import JobSpec

SCHEMA_ID = "https://schemas.neksus.dev/jobspec.v1.json"


def jobspec_json_schema() -> dict[str, Any]:
    """Build JSON Schema for JobSpec with stable metadata fields."""
    schema = JobSpec.model_json_schema()
    schema["$id"] = SCHEMA_ID
    schema["title"] = "Neksus JobSpec"
    schema["x-schema-version"] = 1
    return schema
