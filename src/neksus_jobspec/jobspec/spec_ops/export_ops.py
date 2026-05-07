"""Export operations for JobSpecs."""

from __future__ import annotations

from pathlib import Path

from neksus_jobspec.errors import InvalidInputError
from neksus_jobspec.jobspec.exports import (
    render_generic_json,
    render_generic_xml,
    render_linkedin_ready_json,
)
from neksus_jobspec.jobspec.parser import load_jobspec


def export_jobspec(path: Path, target: str, out: Path) -> dict[str, object]:
    """Export one JobSpec to a deterministic machine-readable format.

    Raises:
        InvalidInputError: If the target export type is unsupported.
    """
    spec = load_jobspec(path)
    warnings: list[str] = []
    if target == "generic-json":
        content = render_generic_json(spec)
    elif target == "generic-xml":
        content = render_generic_xml(spec)
    elif target == "linkedin-ready-json":
        content, warnings = render_linkedin_ready_json(spec)
    else:
        raise InvalidInputError(
            "Unsupported target. Use: generic-json, generic-xml, linkedin-ready-json"
        )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return {
        "ok": True,
        "file": str(path),
        "target": target,
        "output": str(out),
        "warnings": warnings,
    }
