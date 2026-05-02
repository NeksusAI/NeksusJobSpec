# AGENTS.md
This file provides guidance to AI coding agents when working with code in this repository.
## What is Neksus JobSpec?
Neksus JobSpec is a local-first CLI and Python package for creating, validating, inspecting, and rendering structured job specification files.
Users write JobSpecs in YAML. The CLI validates them with Pydantic models and renders them into readable formats such as Markdown. Future versions may expose the same core through FastAPI, local MCP servers, and ChatGPT Skills, but the first implementation is focused on the Python CLI and reusable core library.
The project should remain simple, explicit, and easy to extend.
## Core Pipeline
```text
YAML → PyYAML → Python dict → Pydantic → JobSpec model → Renderer → Markdown

Pipeline stages:

1. Parse
    YAML files are read from disk and converted into Python dictionaries.
2. Validate
    Pydantic validates the input into typed JobSpec models.
3. Inspect
    Metadata is extracted from the validated model for human and JSON output.
4. Render
    The validated JobSpec is rendered to Markdown.
5. Check
    Project-level checks validate config, folders, all JobSpec files, and duplicate IDs.

The CLI must stay thin. Business logic belongs in neksus/core, not in Typer command functions.

Commands

Common development commands:

uv sync
uv run neksus-jobspec version
uv run neksus-jobspec init
uv run neksus-jobspec spec new backend-engineer
uv run neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml
uv run neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml
uv run neksus-jobspec spec inspect jobspecs/backend-engineer.jobspec.yaml
uv run neksus-jobspec check
uv run pytest
uv run ruff check .
uv run ruff format .

Run a single test:

uv run pytest tests/test_cli_spec_validate.py -x

Run tests matching a keyword:

uv run pytest -k "spec_validate" -x

Run linting and formatting checks:

uv run ruff check .
uv run ruff format --check .

Source Layout

Expected repository layout:

neksus/
  __init__.py
  cli/
    __init__.py
    main.py
    commands/
      __init__.py
      init.py
      spec.py
      check.py
      config.py
      version.py
  core/
    __init__.py
    errors.py
    output.py
    project/
      __init__.py
      config.py
      discovery.py
      init_project.py
      checks.py
    jobspec/
      __init__.py
      models.py
      parser.py
      validator.py
      renderer.py
      templates.py
      inspect.py
tests/
  test_cli_init.py
  test_cli_spec_validate.py
  test_cli_spec_render.py
  test_jobspec_models.py
  test_project_checks.py
fixtures/
  valid/
    backend-engineer.jobspec.yaml
  invalid/
    missing-title.jobspec.yaml
    empty-requirements.jobspec.yaml

Architecture Rules

Keep these boundaries strict:

Typer CLI  →  neksus.core

Allowed:

from neksus.core.jobspec.parser import load_jobspec
from neksus.core.jobspec.renderer import render_jobspec

Not allowed:

from neksus.cli.commands.spec import validate

Core modules must never import CLI modules.

The future FastAPI layer should be able to reuse neksus.core without importing Typer, Rich, or CLI command code.

CLI Design

The CLI command name is:

neksus-jobspec

Required command groups:

neksus-jobspec version
neksus-jobspec init
neksus-jobspec spec new NAME
neksus-jobspec spec validate PATH
neksus-jobspec spec render PATH
neksus-jobspec spec schema
neksus-jobspec spec inspect PATH
neksus-jobspec check
neksus-jobspec config get [KEY]
neksus-jobspec config set KEY VALUE

All major commands should support:

--json

JSON output must be stable, plain, and testable. Do not include Rich formatting in JSON mode.

Human output should be concise and readable. Avoid excessive terminal decoration.

Exit Codes

Use stable exit codes:

0 = success
1 = validation or project check failed
2 = CLI usage error
3 = file system error
4 = config error
5 = internal error

Do not introduce new exit codes unless there is a clear need.

JobSpec Model

The core model is defined with Pydantic v2.

Required top-level model:

class JobSpec(BaseModel):
    schema_version: int = 1
    id: str
    title: str
    department: str | None = None
    level: str | None = None
    location: Location | None = None
    summary: str
    responsibilities: list[str]
    requirements: list[str]
    nice_to_have: list[str] = []
    employment: Employment | None = None

Location model:

class Location(BaseModel):
    type: Literal["remote", "hybrid", "onsite"]
    city: str | None = None
    country: str | None = None

Employment model:

class Employment(BaseModel):
    type: Literal["full-time", "part-time", "contract", "internship"]

Validation rules:

* schema_version must currently be 1.
* id must match ^[a-z0-9]+(?:-[a-z0-9]+)*$.
* title must not be empty.
* summary must not be empty.
* responsibilities must contain at least one non-empty string.
* requirements must contain at least one non-empty string.
* nice_to_have must contain only non-empty strings when present.
* location.type must be one of remote, hybrid, or onsite.
* employment.type must be one of full-time, part-time, contract, or internship.

Warnings should be separate from validation errors.

Examples of warnings:

* Very short title.
* Duplicate responsibilities.
* Duplicate requirements.
* Hybrid or onsite role without city/country.

Validation Result Types

Use structured result types for validation and project checks.

Expected shape:

class ValidationIssue(BaseModel):
    path: str
    code: str
    message: str
class ValidationResult(BaseModel):
    valid: bool
    errors: list[ValidationIssue]
    warnings: list[ValidationIssue]
class ProjectCheck(BaseModel):
    name: str
    ok: bool
    message: str
class ProjectCheckResult(BaseModel):
    ok: bool
    checks: list[ProjectCheck]
    errors: list[ValidationIssue]
    warnings: list[ValidationIssue]

Do not return raw Pydantic errors directly from the CLI. Convert them into stable Neksus validation issues.

Project Config

Local project config lives at:

.neksus/config.yaml

Default config:

version: 1
spec_directory: jobspecs
output_directory: dist
default_format: markdown
strict_validation: false

Config rules:

* Discover project root by walking upward until .neksus/config.yaml is found.
* Commands that require a project should fail with config error exit code 4 if no project is found.
* Direct file commands such as spec validate, spec render, and spec inspect should work outside a project.
* spec new --output should work outside a project.
* Only known config keys may be set.

Allowed mutable config keys:

spec_directory
output_directory
default_format
strict_validation

Rendering Rules

Initial supported format:

markdown

Renderer function:

def render_jobspec(spec: JobSpec, format: str = "markdown") -> str:
    ...

Markdown output should be clean and human-readable.

Do not render:

* None
* null
* empty lists
* empty optional sections

Unknown formats must raise UnsupportedFormatError.

Do not add PDF, DOCX, HTML, ATS, or web rendering in the initial CLI implementation.

Error Handling

Define project-specific exceptions:

class NeksusError(Exception): ...
class FileSystemError(NeksusError): ...
class ConfigError(NeksusError): ...
class JobSpecParseError(NeksusError): ...
class JobSpecValidationError(NeksusError): ...
class UnsupportedFormatError(NeksusError): ...

CLI commands should catch expected Neksus exceptions and render controlled errors.

Do not expose raw stack traces for normal user errors such as:

* Missing files
* Invalid YAML
* Invalid JobSpec data
* Missing project config
* Unsupported output format
* Existing files without --force

Unexpected exceptions may still fail normally during development, but production-facing command paths should prefer explicit errors.

Testing

Use pytest.

Use Typer CliRunner for CLI tests.

Tests should not touch the user’s real filesystem. Use temporary directories.

Required coverage:

neksus-jobspec version
neksus-jobspec init
neksus-jobspec init --empty
neksus-jobspec init refuses overwrite
neksus-jobspec spec new backend-engineer
neksus-jobspec spec validate valid fixture
neksus-jobspec spec validate invalid fixture
neksus-jobspec spec validate --json
neksus-jobspec spec render
neksus-jobspec spec render --output
neksus-jobspec spec inspect --json
neksus-jobspec check
duplicate JobSpec IDs fail project check
invalid JobSpec ID fails model validation
empty requirements fail validation

Test names should be explicit.

Good:

def test_spec_validate_returns_zero_for_valid_jobspec() -> None:
    ...

Bad:

def test_validate() -> None:
    ...

Fixtures

Use fixtures for valid and invalid JobSpecs.

Expected fixture layout:

fixtures/
  valid/
    backend-engineer.jobspec.yaml
  invalid/
    missing-title.jobspec.yaml
    empty-requirements.jobspec.yaml

Keep fixtures small and focused.

Do not create large fixture files unless they test a specific behavior.

Code Conventions

Use Python 3.11+.

Use:

str | None
list[str]
dict[str, Any]

Prefer explicit types everywhere.

Every public function should have type annotations.

Keep functions small and boring.

Avoid clever abstractions.

Prefer this:

def slugify_name(name: str) -> str:
    ...

Over this:

class NameProcessor:
    ...

Do not add framework layers before they are needed.

Docstrings

Use docstrings for modules, public classes, and non-obvious functions.

Prefer concise Google-style docstrings.

Example:

def load_jobspec(path: Path) -> JobSpec:
    """Load and validate a JobSpec YAML file.
    Args:
        path: Path to the JobSpec YAML file.
    Returns:
        A validated JobSpec model.
    Raises:
        FileSystemError: If the file cannot be read.
        JobSpecParseError: If the YAML is invalid.
        JobSpecValidationError: If the file does not match the JobSpec schema.
    """

Do not add noisy docstrings to obvious one-line helpers.

Dependency Rules

Use uv.

Prefer:

uv sync
uv run pytest
uv run neksus-jobspec version

Avoid documenting or relying on direct pip or python commands unless needed for packaging compatibility.

Runtime dependencies should remain minimal:

typer
pydantic
PyYAML
rich

Development dependencies:

pytest
ruff
mypy

Do not add heavy dependencies without a clear reason.

Formatting and Linting

Use Ruff for linting and formatting.

Before considering work complete, these should pass:

uv run ruff check .
uv run ruff format --check .
uv run pytest

Mypy should be added when the codebase is stable enough for strict typing.

Implementation Priorities

Build in this order:

1. Package skeleton.
2. Pydantic JobSpec models.
3. YAML parser.
4. Validation result normalization.
5. Markdown renderer.
6. Project config and discovery.
7. neksus-jobspec version.
8. neksus-jobspec init.
9. neksus-jobspec spec validate.
10. neksus-jobspec spec render.
11. neksus-jobspec spec new.
12. neksus-jobspec spec inspect.
13. neksus-jobspec check.
14. neksus-jobspec config get/set.
15. Tests and README.

The first useful milestone is:

neksus-jobspec spec validate jobspecs/example.jobspec.yaml
neksus-jobspec spec render jobspecs/example.jobspec.yaml

Non-Goals

Do not implement these unless explicitly requested:

FastAPI
MCP server
ChatGPT Skill packaging
AI generation
remote sync
authentication
plugin system
PDF export
DOCX export
HTML export
ATS integrations
database storage
web UI

The current goal is a stable local CLI and reusable core.

Agent Behavior Rules

When making changes:

1. Inspect the repository before editing.
2. Prefer small, focused patches.
3. Keep CLI code thin.
4. Keep core code independent from CLI.
5. Add or update tests for behavior changes.
6. Do not silently change the JobSpec schema.
7. Do not introduce new output formats without tests.
8. Do not add dependencies unless justified.
9. Preserve stable JSON output shapes.
10. Preserve stable exit codes.

When unsure, choose the simpler implementation.

Acceptance Criteria

Work is complete only when:

uv sync
uv run neksus-jobspec version
uv run neksus-jobspec init
uv run neksus-jobspec spec new backend-engineer
uv run neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml
uv run neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml
uv run neksus-jobspec check
uv run pytest
uv run ruff check .
uv run ruff format --check .

all succeed.
