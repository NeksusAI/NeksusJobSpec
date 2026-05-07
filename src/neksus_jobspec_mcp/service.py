"""Local MCP service handlers for Neksus JobSpec."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import ValidationError

from neksus_jobspec import __version__
from neksus_jobspec.app import FeedUseCase, ProjectUseCase, SpecUseCase
from neksus_jobspec.errors import ConfigError, FileSystemError, NeksusError
from neksus_jobspec.jobspec.templates import (
    slugify_name,
)
from neksus_jobspec.jobspec.rendering import get_theme_metadata, list_theme_metadata
from neksus_jobspec.project.init_project import init_project


def _error_code(exc: Exception) -> int:
    if isinstance(exc, FileSystemError):
        return 3
    if isinstance(exc, ConfigError):
        return 4
    if isinstance(exc, NeksusError):
        return 1
    if isinstance(exc, ValidationError):
        return 1
    return 5


class JobspecMcpService:
    """Service layer for local MCP tools."""

    def __init__(self) -> None:
        self._feed_use_case = FeedUseCase()
        self._project_use_case = ProjectUseCase()
        self._spec_use_case = SpecUseCase()

    def safe_call(self, fn_name: str, **kwargs: Any) -> dict[str, Any]:
        try:
            fn = getattr(self, fn_name)
            result = fn(**kwargs)
            if isinstance(result, dict):
                return result
            return {"ok": True, "result": result}
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "code": _error_code(exc), "error": str(exc)}

    def version(self) -> dict[str, Any]:
        return {"ok": True, "name": "neksus-jobspec", "version": __version__}

    def init(
        self, root: str | None = None, empty: bool = False, force: bool = False
    ) -> dict[str, Any]:
        project_root = Path(root).resolve() if root else Path.cwd()
        created = init_project(project_root, empty=empty, force=force)
        return {"ok": True, "root": str(project_root), "created": created}

    def check(self, root: str | None = None, strict: bool = False) -> dict[str, Any]:
        project_root = Path(root).resolve() if root else None
        return self._project_use_case.check(root=project_root, strict=strict).model_dump()

    def config_get(self, key: str | None = None, root: str | None = None) -> dict[str, Any]:
        project_root = Path(root).resolve() if root else None
        return self._project_use_case.config_get(key, root=project_root).model_dump(exclude_none=True)

    def config_set(self, key: str, value: str, root: str | None = None) -> dict[str, Any]:
        project_root = Path(root).resolve() if root else None
        return self._project_use_case.config_set(key, value, root=project_root).model_dump()

    def themes_list(self) -> dict[str, Any]:
        return {"ok": True, "themes": [item.model_dump() for item in list_theme_metadata()]}

    def themes_show(self, name: str) -> dict[str, Any]:
        return {"ok": True, "theme": get_theme_metadata(name).model_dump()}

    def spec_schema(self, output: str | None = None) -> dict[str, Any]:
        return self._spec_use_case.write_schema(Path(output) if output else None).model_dump(
            exclude_none=True, by_alias=True
        )

    def spec_templates(self) -> dict[str, Any]:
        return self._spec_use_case.list_templates().model_dump()

    def spec_new(
        self,
        name: str,
        template: str = "basic",
        output: str | None = None,
        force: bool = False,
    ) -> dict[str, Any]:
        slug = slugify_name(name)
        if not slug:
            raise FileSystemError("Name produces an empty slug.")
        target = Path(output) if output else Path.cwd() / f"{slug}.jobspec.yaml"
        return self._spec_use_case.create_new_file(name, template, target, force=force).model_dump()

    def spec_validate(self, path: str, strict: bool = False) -> dict[str, Any]:
        file_path = Path(path)
        return self._spec_use_case.validate_file(file_path, strict=strict).model_dump()

    def spec_render(
        self,
        path: str,
        format: str = "web",
        theme: str | None = None,
        css_path: str | None = None,
        no_css: bool = False,
        asset_base_url: str | None = None,
        output: str | None = None,
        no_validate: bool = False,
    ) -> dict[str, Any]:
        file_path = Path(path)
        if (css_path is not None or no_css or asset_base_url is not None) and format != "web":
            raise ValueError("css_path/no_css/asset_base_url are only supported for web rendering")
        if format not in {"web", "json-ld"}:
            raise ValueError("Unsupported render format. Use: web or json-ld")
        selected_theme = theme or "soft-professional"
        custom_css: str | None = None
        if css_path is not None:
            custom_css = Path(css_path).read_text(encoding="utf-8")
        result = self._spec_use_case.render_file(
            file_path,
            format=format,
            theme=selected_theme,
            no_validate=no_validate,
            embed_css=not no_css,
            custom_css=custom_css,
            asset_base_url=asset_base_url,
            output=Path(output) if output else None,
        )
        return result.model_dump(exclude_none=True)

    def spec_inspect(self, path: str) -> dict[str, Any]:
        file_path = Path(path)
        return self._spec_use_case.inspect_file(file_path).model_dump()

    def spec_status(self, path: str) -> dict[str, Any]:
        file_path = Path(path)
        return self._spec_use_case.status_file(file_path).model_dump()

    def spec_migrate(self, path: str, write: bool = False) -> dict[str, Any]:
        file_path = Path(path)
        result = self._spec_use_case.migrate_status(file_path).model_dump()
        if write:
            return {
                "ok": False,
                "file": str(file_path),
                "error": "Write mode is not implemented for schema migrations.",
            }
        ok = result["status"] == "already_current"
        return {"ok": ok, "file": str(file_path), **result}

    def spec_export(self, path: str, target: str, out: str) -> dict[str, Any]:
        file_path = Path(path)
        if target not in {"generic-json", "generic-xml", "linkedin-ready-json"}:
            raise ValueError(
                "Unsupported target. Use: generic-json, generic-xml, linkedin-ready-json"
            )
        return self._spec_use_case.export_file(file_path, target, Path(out)).model_dump()

    def feed_export(
        self,
        inputs: list[str],
        target: str,
        out: str,
        skip_invalid: bool = False,
    ) -> dict[str, Any]:
        return self._feed_use_case.export(
            inputs=inputs,
            target=target,
            out=Path(out),
            skip_invalid=skip_invalid,
        )

    def feed_sitemap(
        self,
        inputs: list[str],
        base_url: str,
        out: str,
        exclude_closed: bool = False,
    ) -> dict[str, Any]:
        return self._feed_use_case.sitemap(
            inputs=inputs,
            base_url=base_url,
            out=Path(out),
            exclude_closed=exclude_closed,
        )
