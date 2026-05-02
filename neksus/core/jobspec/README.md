# `neksus.core.jobspec`

JobSpec-centric domain logic.

## End-to-end flow

1. `parser.load_yaml_file(path)`
   - Reads YAML and enforces mapping shape.
   - Raises domain-specific parse/filesystem errors.

2. `validator.validate_spec_data(data)`
   - Validates against Pydantic model.
   - Normalizes schema errors into `ValidationIssue` entries.
   - Adds non-fatal warnings (short title, duplicates, missing location detail).

3. `renderer.render_jobspec(spec, format="markdown")`
   - Converts a validated model into markdown or html.
   - Omits empty optional sections.

4. `schema.jobspec_json_schema()`
   - Exports JSON Schema derived from the Pydantic model.
   - Adds schema metadata fields (`$id`, title, version marker).

4. `inspect.inspect_jobspec(spec, validation)`
   - Produces normalized metadata for CLI and JSON output.

## Modules

- `models.py`
  - `JobSpec`, `Location`, `Employment`.
  - Core schema constraints and field validators.

- `parser.py`
  - YAML parsing and model loading helpers.

- `validator.py`
  - Validation error normalization and warnings logic.
  - `pydantic_errors_to_issues(...)` gives stable, CLI-safe issue shapes.

- `renderer.py`
  - Markdown + HTML renderer and humanized value formatting.

- `schema.py`
  - JSON Schema export helper for editor/tooling integration.

- `templates.py`
  - `slugify_name(...)`, `title_from_name(...)`, `build_jobspec_template(...)`.

- `inspect.py`
  - Normalized metadata extraction with counts and validity status.

## Validation philosophy

- Errors are blocking and fail validation.
- Warnings are advisory by default.
- Strict mode can elevate warnings to failures at command/check level.
