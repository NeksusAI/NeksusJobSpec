"""JSON renderer."""

from __future__ import annotations

from neksus_jobspec.jobspec.rendering.normalize import normalized_json_payload
from neksus_jobspec.output import to_json


def render_json(spec) -> str:
    """Render a JobSpec into normalized JSON."""
    return to_json(normalized_json_payload(spec))
