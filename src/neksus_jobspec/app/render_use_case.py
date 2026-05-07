"""Project batch render use case."""

from __future__ import annotations

from pathlib import Path

from neksus_jobspec.app.dtos import RenderBatchResult
from neksus_jobspec.app.filesystem import FileSystemGateway
from neksus_jobspec.app.project_context import ProjectContext
from neksus_jobspec.errors import ConfigError, FileSystemError, InvalidInputError
from neksus_jobspec.jobspec.models import JobSpec
from neksus_jobspec.jobspec.parser import load_yaml_file
from neksus_jobspec.jobspec.renderer import render_jobspec
from neksus_jobspec.jobspec.validator import validate_spec_data
from neksus_jobspec.project.config import ProjectConfig, RenderProfile

EXTENSIONS_BY_FORMAT = {"web": ".html", "json-ld": ".json"}


class RenderUseCase:
    """Orchestrates project-level batch render flows."""

    def __init__(self, fs: FileSystemGateway | None = None) -> None:
        """Initialize with a filesystem gateway for side-effect isolation."""
        self._fs = fs or FileSystemGateway()

    def render_project(
        self,
        *,
        root: Path | None = None,
        format: str | None = None,
        theme: str | None = None,
        css: Path | None = None,
        no_css: bool = False,
        asset_base_url: str | None = None,
        profile: str | None = None,
        clean: bool = False,
    ) -> RenderBatchResult:
        """Render all project JobSpecs with resolved profile/config options.

        This method centralizes option precedence, validation checks, and
        deterministic output writing so CLI and other callers do not duplicate
        batch rendering orchestration logic.
        """
        context = ProjectContext.discover(root)
        selected_profile = self._resolve_profile(profile, context.config)

        render_format = (
            format
            or (selected_profile.format if selected_profile else None)
            or context.config.default_format
        )
        selected_theme = (
            theme
            or (selected_profile.theme if selected_profile else None)
            or context.config.default_theme
        )
        output_directory = (
            selected_profile.output_directory if selected_profile else None
        ) or context.config.output_directory
        sections = (
            selected_profile.sections.model_dump()
            if selected_profile and selected_profile.sections
            else None
        )

        if (css is not None or no_css or asset_base_url is not None) and render_format != "web":
            raise InvalidInputError(
                "--css, --no-css, and --asset-base-url are only supported for --format web"
            )
        if render_format not in EXTENSIONS_BY_FORMAT:
            raise InvalidInputError(f"Unsupported render format: {render_format}")

        custom_css: str | None = None
        if css is not None:
            try:
                custom_css = self._fs.read_text(css)
            except OSError as exc:
                raise FileSystemError(f"Failed to read CSS file: {css}") from exc

        spec_dir = context.root / context.config.spec_directory
        output_dir = context.root / output_directory
        if not spec_dir.exists() or not spec_dir.is_dir():
            raise FileSystemError(f"Spec directory does not exist: {spec_dir}")

        if clean and output_dir.exists():
            self._fs.remove_tree(output_dir)
        self._fs.mkdir(output_dir)

        files = sorted(spec_dir.glob("*.jobspec.yaml"))
        rendered: list[dict[str, str]] = []
        errors: list[dict[str, str]] = []
        warnings: list[dict[str, str]] = []

        for path in files:
            data = load_yaml_file(path)
            validation = validate_spec_data(data)

            for issue in validation.errors:
                errors.append({"source": str(path.relative_to(context.root)), **issue.model_dump()})
            for issue in validation.warnings:
                warnings.append({"source": str(path.relative_to(context.root)), **issue.model_dump()})
            if not validation.valid:
                continue

            target_name = self._output_name_for_data(data, path)
            target = output_dir / f"{target_name}{EXTENSIONS_BY_FORMAT[render_format]}"
            spec = JobSpec.model_validate(data)
            rendered_content = render_jobspec(
                spec,
                format=render_format,
                theme=selected_theme,
                embed_css=not no_css,
                custom_css=custom_css,
                asset_base_url=asset_base_url,
                sections=sections,
            )
            self._fs.write_text(target, rendered_content)
            if render_format == "web":
                self._fs.write_text(target.with_suffix(".css"), spec.rendering.web.css.inline)
            rendered.append(
                {
                    "source": str(path.relative_to(context.root)),
                    "output": str(target.relative_to(context.root)),
                }
            )

        return RenderBatchResult(
            ok=not errors,
            format=render_format,
            theme=selected_theme,
            profile=profile,
            rendered=rendered,
            errors=errors,
            warnings=warnings,
        )

    @staticmethod
    def _output_name_for_data(data: dict, source: Path) -> str:
        """Derive stable output basename from spec id or source filename."""
        spec_id = data.get("id")
        if isinstance(spec_id, str) and spec_id.strip():
            return spec_id.strip()
        return source.stem

    @staticmethod
    def _resolve_profile(name: str | None, config: ProjectConfig) -> RenderProfile | None:
        """Resolve a named render profile from project config."""
        if name is None:
            return None
        profile = config.render_profiles.get(name)
        if profile is None:
            raise ConfigError(f"Unknown render profile: {name}")
        return profile
