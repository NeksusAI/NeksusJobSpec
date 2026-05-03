# Versioning and Compatibility Policy

## Versioning approach

Neksus JobSpec follows semantic versioning after the initial `0.1.0` release.

During `0.x` releases, public APIs are intended to be usable but may still evolve.

## Compatibility contract

### Stable public Python API

Compatibility applies to top-level imports from `neksus_jobspec`:

```python
from neksus_jobspec import JobSpec, load_jobspec, validate_jobspec, render_jobspec
```

### Stable CLI surface

CLI compatibility applies to documented commands in the [CLI Reference](cli-reference.md).

### Stable JobSpec schema surface

Schema compatibility applies to documented fields in [JobSpec Format](specification.md) and generated schema output.

## Non-stable internals

Internal modules under `neksus.core.*` and `neksus.cli.*` are not guaranteed stable.

## Breaking changes and deprecations

Breaking changes should be documented in release notes.

When practical, deprecations should be used before removals.

## Out of current contract

Hosted API and MCP capabilities are planned but are not part of the current compatibility contract.
