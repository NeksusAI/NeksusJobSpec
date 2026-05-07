"""Typed response DTOs for app-layer use cases."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ValidateFileResult(BaseModel):
    ok: bool
    file: str
    valid: bool
    errors: list[dict[str, str]]
    warnings: list[dict[str, str]]


class RenderFileResult(BaseModel):
    ok: bool
    file: str
    format: str
    theme: str
    output: str | None = None
    content: str | None = None
    valid: bool | None = None
    errors: list[dict[str, str]] | None = None
    warnings: list[dict[str, str]] | None = None


class ProjectCheckResultDTO(BaseModel):
    ok: bool
    checks: list[dict[str, Any]]
    errors: list[dict[str, str]]
    warnings: list[dict[str, str]]


class ConfigGetResult(BaseModel):
    ok: bool
    key: str | None = None
    value: Any = None
    config: dict[str, Any] | None = None


class ConfigSetResult(BaseModel):
    ok: bool
    config: dict[str, Any]


class GenericOkPayload(BaseModel):
    ok: bool = True


class RenderBatchResult(BaseModel):
    ok: bool
    format: str
    theme: str
    profile: str | None = None
    rendered: list[dict[str, str]]
    errors: list[dict[str, str]]
    warnings: list[dict[str, str]]


class TemplateListResult(BaseModel):
    ok: bool
    templates: list[str]


class SchemaResult(BaseModel):
    ok: bool
    format: str
    schema_version: int
    output: str | None = None
    schema_payload: dict[str, Any] | None = Field(
        default=None,
        validation_alias="schema",
        serialization_alias="schema",
    )


class NewFileResult(BaseModel):
    ok: bool
    file: str
    template: str


class MigrateStatusResult(BaseModel):
    schema_version: int | None = None
    current_schema_version: int
    status: str
    message: str
    upgradable: bool


class InspectResult(BaseModel):
    ok: bool
    file: str
    metadata: dict[str, Any]


class StatusResult(BaseModel):
    ok: bool
    file: str
    id: str
    title: str
    campaign_status: str | None = None
    starts_at: str | None = None
    expires_at: str | None = None
    days_remaining: int | None = None


class ExportResult(BaseModel):
    ok: bool
    file: str
    target: str
    output: str
    warnings: list[str]
