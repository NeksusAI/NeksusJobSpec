# Security Policy

## Supported versions

Security fixes are applied to the latest published release line (`0.4.x`) and the default branch.

## Reporting a vulnerability

Please report suspected vulnerabilities privately to the repository owner through a non-public channel.

Include:

- affected version (`neksus-jobspec version`)
- reproduction steps
- impact assessment
- proof-of-concept input/files (if safe to share)

Do not open public issues for unpatched vulnerabilities.

## Response targets

- Initial acknowledgment: within 3 business days
- Triage decision: within 10 business days
- Fix timeline: depends on severity and release risk

## Scope

In-scope:

- CLI command handling and file I/O
- YAML parsing/validation paths
- renderer output safety boundaries
- dependency-related security issues

Out-of-scope:

- hypothetical attacks requiring local machine compromise first
- vulnerabilities in unsupported versions

## Disclosure

After a fix is available, relevant details are documented in:

- `CHANGELOG.md` (`Security` section when applicable)
- `docs/project/release-notes.md`
