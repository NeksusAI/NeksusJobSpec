# JobSpec Format

This page explains the human-facing JobSpec format and how to think about it when authoring role definitions.

Neksus currently validates the `JobSpec` core model fields in `schema_version: 1`. Some broader hiring-document sections listed below are currently modeled directly, while others are planned structure layers for future schema revisions.

## Current core sections (available now)

- role identity (`id`, `title`, optional `department`, optional `level`)
- location (`location`)
- employment (`employment`)
- role summary (`summary`)
- responsibilities (`responsibilities`)
- requirements (`requirements`)
- optional preferences (`nice_to_have`)

## Extended sections (planned)

These sections are commonly needed in production hiring workflows and are candidates for future schema expansion:

- company
- compensation
- benefits
- application process
- metadata

Planned means these are not first-class schema fields in the current stable model unless represented in existing free-text sections.

## Authoring guidelines

- Keep each responsibility and requirement as a single clear statement.
- Prefer concise bullet items over long paragraphs.
- Keep role identity stable over time to preserve diff quality.
- Use explicit location and employment type where applicable.

For exact field definitions and constraints, see [Schema](schema.md).
