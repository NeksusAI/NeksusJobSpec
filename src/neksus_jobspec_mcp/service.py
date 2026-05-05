"""Local MCP service handlers for Neksus JobSpec."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from neksus_jobspec import __version__
from neksus_jobspec.errors import ConfigError, FileSystemError, NeksusError
from neksus_jobspec.jobspec.exports import (
    render_generic_json,
    render_generic_xml,
    render_linkedin_ready_json,
)
from neksus_jobspec.jobspec.feeds import (
    expand_input_paths,
    render_jobs_json_feed,
    render_jobs_xml_feed,
    render_sitemap,
)
from neksus_jobspec.jobspec.inspect import inspect_jobspec
from neksus_jobspec.jobspec.migrate import inspect_schema_version
from neksus_jobspec.jobspec.models import JobSpec
from neksus_jobspec.jobspec.parser import load_jobspec, load_yaml_file
from neksus_jobspec.jobspec.renderer import render_jobspec
from neksus_jobspec.jobspec.schema import jobspec_json_schema
from neksus_jobspec.jobspec.templates import (
    build_jobspec_template,
    dump_jobspec_yaml,
    list_template_names,
    slugify_name,
)
from neksus_jobspec.jobspec.validator import validate_spec_data, validate_spec_model
from neksus_jobspec.jobspec.rendering import get_theme_metadata, list_theme_metadata
from neksus_jobspec.output import to_json
from neksus_jobspec.project.checks import run_project_checks
from neksus_jobspec.project.config import load_project_config, set_config_key
from neksus_jobspec.project.discovery import find_project_root
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


def _days_remaining(expires_at: date | None) -> int | None:
    if not expires_at:
        return None
    return (expires_at - date.today()).days


class JobspecMcpService:
    """Service layer for local MCP tools."""

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
        project_root = find_project_root(Path(root).resolve() if root else None)
        result = run_project_checks(project_root, strict=strict)
        return {
            "ok": result.ok,
            "checks": [item.model_dump() for item in result.checks],
            "errors": [item.model_dump() for item in result.errors],
            "warnings": [item.model_dump() for item in result.warnings],
        }

    def config_get(self, key: str | None = None, root: str | None = None) -> dict[str, Any]:
        project_root = find_project_root(Path(root).resolve() if root else None)
        config = load_project_config(project_root).model_dump()
        if key is None:
            return {"ok": True, "config": config}
        if key not in config:
            raise ValueError(f"Unknown config key: {key}")
        return {"ok": True, "key": key, "value": config[key]}

    def config_set(self, key: str, value: str, root: str | None = None) -> dict[str, Any]:
        project_root = find_project_root(Path(root).resolve() if root else None)
        updated = set_config_key(project_root, key, value)
        return {"ok": True, "config": updated.model_dump()}

    def themes_list(self) -> dict[str, Any]:
        return {"ok": True, "themes": [item.model_dump() for item in list_theme_metadata()]}

    def themes_show(self, name: str) -> dict[str, Any]:
        return {"ok": True, "theme": get_theme_metadata(name).model_dump()}

    def spec_schema(self, output: str | None = None) -> dict[str, Any]:
        schema = jobspec_json_schema()
        if output:
            target = Path(output)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(to_json(schema), encoding="utf-8")
            return {"ok": True, "format": "json-schema", "schema_version": 1, "output": str(target)}
        return {"ok": True, "format": "json-schema", "schema_version": 1, "schema": schema}

    def spec_templates(self) -> dict[str, Any]:
        return {"ok": True, "templates": list(list_template_names())}

    def spec_new(
        self,
        name: str,
        template: str = "basic",
        output: str | None = None,
        force: bool = False,
    ) -> dict[str, Any]:
        if template not in list_template_names():
            raise ValueError(f"Unknown template: {template}")
        slug = slugify_name(name)
        if not slug:
            raise FileSystemError("Name produces an empty slug.")
        target = Path(output) if output else Path.cwd() / f"{slug}.jobspec.yaml"
        if target.exists() and not force:
            raise FileSystemError(f"File already exists: {target}. Use force=true to overwrite.")
        target.parent.mkdir(parents=True, exist_ok=True)
        template_data = build_jobspec_template(name, template=template)
        JobSpec.model_validate(template_data)
        target.write_text(dump_jobspec_yaml(template_data), encoding="utf-8")
        return {"ok": True, "file": str(target), "template": template}

    def spec_validate(self, path: str, strict: bool = False) -> dict[str, Any]:
        file_path = Path(path)
        data = load_yaml_file(file_path)
        result = validate_spec_data(data)
        ok = result.valid and not (strict and result.warnings)
        return {
            "ok": ok,
            "file": str(file_path),
            "valid": result.valid,
            "errors": [issue.model_dump() for issue in result.errors],
            "warnings": [issue.model_dump() for issue in result.warnings],
        }

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
        spec = load_jobspec(file_path)
        validation = validate_spec_model(spec)
        if not no_validate and not validation.valid:
            return {
                "ok": False,
                "file": str(file_path),
                "valid": False,
                "errors": [issue.model_dump() for issue in validation.errors],
                "warnings": [issue.model_dump() for issue in validation.warnings],
            }
        selected_theme = theme or "soft-professional"
        custom_css: str | None = None
        if css_path is not None:
            custom_css = Path(css_path).read_text(encoding="utf-8")
        content = render_jobspec(
            spec,
            format=format,
            theme=selected_theme,
            embed_css=not no_css,
            custom_css=custom_css,
            asset_base_url=asset_base_url,
        )
        if output:
            target = Path(output)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            return {
                "ok": True,
                "file": str(file_path),
                "format": format,
                "theme": selected_theme,
                "output": str(target),
            }
        return {
            "ok": True,
            "file": str(file_path),
            "format": format,
            "theme": selected_theme,
            "content": content,
        }

    def spec_inspect(self, path: str) -> dict[str, Any]:
        file_path = Path(path)
        spec = load_jobspec(file_path)
        validation = validate_spec_model(spec)
        metadata = inspect_jobspec(spec, validation)
        return {"ok": True, "file": str(file_path), "metadata": metadata}

    def spec_status(self, path: str) -> dict[str, Any]:
        file_path = Path(path)
        spec = load_jobspec(file_path)
        campaign = spec.campaign
        return {
            "ok": True,
            "file": str(file_path),
            "id": spec.id,
            "title": spec.job.title,
            "campaign_status": campaign.status if campaign else None,
            "starts_at": campaign.starts_at.isoformat()
            if campaign and campaign.starts_at
            else None,
            "expires_at": campaign.expires_at.isoformat()
            if campaign and campaign.expires_at
            else None,
            "days_remaining": _days_remaining(campaign.expires_at) if campaign else None,
        }

    def spec_migrate(self, path: str, write: bool = False) -> dict[str, Any]:
        file_path = Path(path)
        result = inspect_schema_version(file_path)
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
        output = Path(out)
        spec = load_jobspec(file_path)
        warnings: list[str] = []
        if target == "generic-json":
            content = render_generic_json(spec)
        elif target == "generic-xml":
            content = render_generic_xml(spec)
        elif target == "linkedin-ready-json":
            content, warnings = render_linkedin_ready_json(spec)
        else:
            raise ValueError(
                "Unsupported target. Use: generic-json, generic-xml, linkedin-ready-json"
            )
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")
        return {
            "ok": True,
            "file": str(file_path),
            "target": target,
            "output": str(output),
            "warnings": warnings,
        }

    def feed_export(
        self,
        inputs: list[str],
        target: str,
        out: str,
        skip_invalid: bool = False,
    ) -> dict[str, Any]:
        paths = expand_input_paths(inputs)
        if not paths:
            raise ValueError("No input files found.")
        specs = []
        invalid: list[str] = []
        for path in paths:
            try:
                specs.append(load_jobspec(path))
            except Exception:  # noqa: BLE001
                invalid.append(str(path))
        if invalid and not skip_invalid:
            raise NeksusError(f"Invalid JobSpec input(s): {', '.join(invalid)}")
        if target == "jobs-json":
            content = render_jobs_json_feed(specs)
        elif target == "jobs-xml":
            content = render_jobs_xml_feed(specs)
        else:
            raise ValueError("Unsupported target. Use: jobs-json or jobs-xml")
        output = Path(out)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")
        return {
            "ok": True,
            "target": target,
            "output": str(output),
            "count": len(specs),
            "invalid": invalid,
        }

    def feed_sitemap(
        self,
        inputs: list[str],
        base_url: str,
        out: str,
        exclude_closed: bool = False,
    ) -> dict[str, Any]:
        paths = expand_input_paths(inputs)
        if not paths:
            raise ValueError("No input files found.")
        specs = [load_jobspec(path) for path in paths]
        content = render_sitemap(specs, base_url, exclude_closed=exclude_closed)
        output = Path(out)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")
        return {
            "ok": True,
            "output": str(output),
            "count": len(specs),
            "exclude_closed": exclude_closed,
        }
