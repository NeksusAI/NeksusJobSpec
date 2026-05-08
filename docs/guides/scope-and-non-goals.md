# Scope and Non-Goals

This page is the canonical user-facing boundary for the free/core package.

## In scope

- local-first CLI (`neksus-jobspec`)
- local Python API (`neksus_jobspec`)
- local rendering (`web`, `json-ld`)
- deterministic exports (`generic-json`, `generic-xml`, `linkedin-ready-json`)
- multi-job feeds (`jobs-json`, `jobs-xml`)
- sitemap generation
- optional local stdio MCP server

## Out of scope

- hosted SaaS/API infrastructure
- authentication/authorization
- database persistence
- application forms/candidate intake
- CV upload/parsing
- ATS workflow automation
- payments
- direct LinkedIn API posting

## Important clarification

`linkedin-ready-json` is an output profile only. It does not publish jobs to LinkedIn.
