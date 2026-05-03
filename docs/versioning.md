# Versioning and Compatibility Policy

## Semantic versioning

Neksus JobSpec follows semantic versioning.

During `0.x`, public APIs are intended to be usable but may still evolve between minor releases.

## Compatibility surface

### Stable public Python API

Stable imports are exposed from `neksus_jobspec`:

```python
from neksus_jobspec import JobSpec, load_jobspec, validate_jobspec, render_jobspec
```

`__version__` is also stable for tooling and diagnostics.

### Stable CLI surface

Documented CLI commands are part of the compatibility contract.

### Stable schema surface

Documented JobSpec schema fields are part of the compatibility contract.

Documented component types and variants are part of the compatibility contract once released.

## Non-stable internals

Internal modules under `neksus.core.*` and `neksus.cli.*` are implementation details and not stable contracts.

## Breaking changes and deprecations

Breaking changes must be documented in `CHANGELOG.md`.

Deprecations should be preferred before removals when practical.

## Out of scope for v0.2.0 contract

Hosted API and MCP capabilities are planned but are not part of the v0.2.0 compatibility contract.
