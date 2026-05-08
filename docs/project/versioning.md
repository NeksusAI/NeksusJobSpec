# Versioning and Compatibility Policy

## SemVer policy

Neksus JobSpec follows semantic versioning. During `0.x`, evolution is allowed, but documented CLI/schema/API surfaces are treated as contracts.

## Compatibility surfaces

- Stable public Python imports from `neksus_jobspec`
- Documented CLI commands/options
- Documented schema fields and component contracts
- Optional local MCP surface when `mcp` extra is installed

## Current line

This docs set targets `v0.4.x`.

## Breaking changes

Breaking changes must be explicit in:
- `CHANGELOG.md`
- release notes
- schema/reference docs

## Non-stable internals

Internal implementation modules may change without API guarantees.

## Product boundary

The compatibility contract does not include hosted SaaS, auth, database persistence, candidate/CV workflows, payments, or direct LinkedIn posting.
