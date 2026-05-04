# Rendering

Neksus v0.2.x renders component-based JobSpecs to `web` and `json-ld`.

## Input model

Rendering expects a v0.2.x component JobSpec (`page` + `job` + `components`).

## Web

- `soft-professional` is pinned to the Stitch screen contract.
- Canonical HTML fixture: `fixtures/stitch/isolated-jobspec-output.soft-professional.html`.
- Canonical screenshot fixture: `fixtures/stitch/isolated-jobspec-output.soft-professional.png`.
- CLI/theme entry points stay the same (`spec render`, `render`, `--theme soft-professional`).
- JSON-LD output remains model-driven; only web output is contract-pinned.

## JSON-LD

- Outputs `schema.org` `JobPosting` JSON-LD from the validated model.

## Security boundaries

- CSS settings are trusted local-output settings.
- Rendering emits output only; it does not execute scripts.
- Rendering does not fetch external resources.
