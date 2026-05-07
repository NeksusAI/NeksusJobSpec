# Versioning and Compatibility Policy

## Semantic versioning

Neksus JobSpec follows semantic versioning.

During `0.x`, public APIs are intended to be usable but may still evolve
between minor releases.

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

Documented component types, variants, and placement fields are part of the
compatibility contract once released.

### Stable local MCP surface (optional)

In `v0.3.x`, local stdio MCP support is part of the release contract when the
optional `mcp` extra is installed.

- Install extra: `neksus-jobspec[mcp]`
- Console script: `neksus-jobspec-mcp`
- Scope: local-only CLI/API-parity tools

The MCP server is not a hosted API and is not an ATS or direct platform posting
integration.

## Breaking changes and cleanup

`0.3.x` contains a breaking cleanup relative to early/transitional `0.2.0`
compatibility behavior.

Legacy simple-schema payloads are removed and component schema is authoritative.

Breaking changes must be documented in `CHANGELOG.md`.

Deprecations should be preferred before removals when practical.

## Non-stable internals

Internal modules under `neksus_jobspec.*` and `neksus_jobspec_cli.*` are
implementation details and not stable contracts.

## Out of scope for v0.3.x contract

Hosted API capabilities are planned but are not part of the v0.3.x
compatibility contract.

v0.3.x does not include application forms, application collection, CV upload,
CV parsing, candidate storage, email delivery, payments, hosted APIs,
or ATS workflows.
