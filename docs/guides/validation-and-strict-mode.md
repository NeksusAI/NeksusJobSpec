# Validation and Strict Mode

Validation separates hard errors from soft warnings.

## Errors

Errors fail validation immediately (exit code `1` for validate/check failures).

## Warnings

Warnings are advisory by default:
- very short title
- duplicate responsibilities
- duplicate requirements
- hybrid/onsite role missing both city and country

## Strict mode

Use strict mode to treat warnings as failures:

```bash
neksus-jobspec spec validate jobspecs/example.jobspec.yaml --strict
neksus-jobspec check --strict
```

Project config can also enforce strict mode with `strict_validation: true`.
