# Code Structure

This page indexes the internal package structure for maintainers.

## Source package map

- Core package: `src/neksus_jobspec/README.md`
- App use cases: `src/neksus_jobspec/app/README.md`
- JobSpec domain: `src/neksus_jobspec/jobspec/README.md`
- JobSpec operation slices: `src/neksus_jobspec/jobspec/spec_ops/README.md`
- Rendering internals: `src/neksus_jobspec/jobspec/rendering/README.md`
- Project internals: `src/neksus_jobspec/project/README.md`
- CLI package: `src/neksus_jobspec_cli/README.md`
- CLI commands: `src/neksus_jobspec_cli/commands/README.md`
- MCP package: `src/neksus_jobspec_mcp/README.md`

## Layering contract

- `CLI/MCP -> app use cases -> jobspec/project domain`
- App layer owns orchestration and typed DTO payload contracts.
- Domain modules own parsing, model validation, rendering, and exports.

## Notes

Internal module APIs may change between versions. For stable automation behavior, prefer the CLI contract.
