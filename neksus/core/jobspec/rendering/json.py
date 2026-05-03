"""JSON renderer."""

from __future__ import annotations

from neksus.core.jobspec.models import JobSpec
from neksus.core.output import to_json


def render_json(spec: JobSpec) -> str:
    """Render a JobSpec into normalized JSON."""
    return to_json(spec.model_dump())
