"""Create/list operations for JobSpecs."""

from __future__ import annotations

from pathlib import Path

from neksus_jobspec.errors import FileSystemError, InvalidInputError
from neksus_jobspec.jobspec.models import JobSpec
from neksus_jobspec.jobspec.templates import (
    build_jobspec_template,
    dump_jobspec_yaml,
    list_template_names,
)


def list_templates() -> list[str]:
    """Return built-in template names."""
    return list(list_template_names())


def create_jobspec_file(
    name: str, template: str, target: Path, force: bool = False
) -> dict[str, str | bool]:
    """Create a new JobSpec file from a template.

    Raises:
        InvalidInputError: If the template is unknown.
        FileSystemError: If output exists and force is disabled.
    """
    templates = list_templates()
    if template not in templates:
        raise InvalidInputError(f"Unknown template: {template}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not force:
        raise FileSystemError(f"File already exists: {target}. Use force=true to overwrite.")
    template_data = build_jobspec_template(name, template=template)
    JobSpec.model_validate(template_data)
    target.write_text(dump_jobspec_yaml(template_data), encoding="utf-8")
    return {"ok": True, "file": str(target), "template": template}
