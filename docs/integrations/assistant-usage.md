# Assistant Usage Guidance

## Preferred workflow

1. Generate typed JobSpec YAML.
2. Run `spec validate`.
3. Run `spec lint`.
4. Use `spec render` (`web`/`json-ld`) or `spec export` targets.

## Components-first rule

Assistants should emit typed `components` data, not arbitrary HTML blocks.

## Trust boundaries

- Keep behavior in YAML/theme packages.
- Do not assume JavaScript runtime logic for rendering behavior.
- Output is deterministic text artifacts, not executable app code.

## Useful command sequence

```bash
neksus-jobspec spec validate job.jobspec.yaml
neksus-jobspec spec lint job.jobspec.yaml
neksus-jobspec spec render job.jobspec.yaml --format json-ld
```
