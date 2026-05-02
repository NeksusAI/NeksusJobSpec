"""JobSpec domain public API."""

from neksus.core.jobspec.models import Employment, JobSpec, Location
from neksus.core.jobspec.parser import load_jobspec, load_yaml_file
from neksus.core.jobspec.renderer import render_jobspec
from neksus.core.jobspec.schema import jobspec_json_schema
from neksus.core.jobspec.validator import (
    collect_warnings,
    pydantic_errors_to_issues,
    validate_spec_data,
    validate_spec_model,
)

__all__ = [
    "Employment",
    "JobSpec",
    "Location",
    "collect_warnings",
    "load_jobspec",
    "load_yaml_file",
    "jobspec_json_schema",
    "pydantic_errors_to_issues",
    "render_jobspec",
    "validate_spec_data",
    "validate_spec_model",
]
