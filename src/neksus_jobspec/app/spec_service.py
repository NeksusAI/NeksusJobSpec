"""Application service for JobSpec validate/render operations."""

from __future__ import annotations

from pathlib import Path

from neksus_jobspec.app.project_context import ProjectContext
from neksus_jobspec.app.dtos import (
    ExportResult,
    InspectResult,
    MigrateStatusResult,
    NewFileResult,
    RenderFileResult,
    SchemaResult,
    StatusResult,
    TemplateListResult,
    ValidateFileResult,
)
from neksus_jobspec.errors import ConfigError, FileSystemError
from neksus_jobspec.jobspec.spec_ops import (
    create_jobspec_file,
    export_jobspec,
    inspect_jobspec_file,
    list_templates,
    migrate_status,
    render_jobspec_file,
    status_jobspec_file,
    validate_jobspec_file,
    write_schema,
)
from neksus_jobspec.jobspec.templates import slugify_name


class SpecUseCase:
    """Use-case orchestration for JobSpec read/validate/render flows."""

    def resolve_new_path(self, name: str, output: Path | None) -> Path:
        """Resolve output path for spec creation with project-aware fallback."""
        slug = slugify_name(name)
        if not slug:
            raise FileSystemError("Name produces an empty slug.")
        if output:
            return output
        try:
            context = ProjectContext.discover()
            return context.root / context.config.spec_directory / f"{slug}.jobspec.yaml"
        except ConfigError:
            return Path.cwd() / f"{slug}.jobspec.yaml"

    def resolve_default_theme(self, explicit_theme: str | None) -> str:
        """Resolve render theme using project config when no explicit value is set."""
        if explicit_theme:
            return explicit_theme
        try:
            context = ProjectContext.discover()
            return context.config.default_theme
        except ConfigError:
            return "soft-professional"

    def list_templates(self) -> TemplateListResult:
        """List built-in template names as a typed payload."""
        return TemplateListResult(ok=True, templates=list_templates())

    def write_schema(self, output: Path | None = None) -> SchemaResult:
        """Return or write JSON Schema for JobSpec as a typed payload."""
        return SchemaResult.model_validate(write_schema(output))

    def create_new_file(
        self, name: str, template: str, target: Path, force: bool = False
    ) -> NewFileResult:
        """Create a new JobSpec file from a named template."""
        return NewFileResult.model_validate(
            create_jobspec_file(name, template, target, force=force)
        )

    def migrate_status(self, path: Path) -> MigrateStatusResult:
        """Inspect schema migration status for a specific JobSpec file."""
        return MigrateStatusResult.model_validate(migrate_status(path))

    def validate_file(self, path: Path, strict: bool = False) -> ValidateFileResult:
        """Validate a JobSpec YAML file and return normalized issues/warnings."""
        return ValidateFileResult.model_validate(validate_jobspec_file(path, strict=strict))

    def inspect_file(self, path: Path) -> InspectResult:
        """Inspect metadata for a validated JobSpec file."""
        return InspectResult.model_validate(inspect_jobspec_file(path))

    def status_file(self, path: Path) -> StatusResult:
        """Return campaign status metadata for a specific JobSpec file."""
        return StatusResult.model_validate(status_jobspec_file(path))

    def export_file(self, path: Path, target: str, out: Path) -> ExportResult:
        """Export a JobSpec into a deterministic machine-readable target."""
        return ExportResult.model_validate(export_jobspec(path, target, out))

    def render_file(
        self,
        path: Path,
        *,
        format: str,
        theme: str,
        no_validate: bool,
        embed_css: bool,
        custom_css: str | None,
        asset_base_url: str | None,
        output: Path | None,
    ) -> RenderFileResult:
        """Render a JobSpec file and return output metadata/content payload."""
        payload = render_jobspec_file(
            path,
            format=format,
            theme=theme,
            no_validate=no_validate,
            embed_css=embed_css,
            custom_css=custom_css,
            asset_base_url=asset_base_url,
            output=output,
        )
        return RenderFileResult.model_validate(payload)
