# neksus_jobspec.app

Application-layer orchestration for the core package.

## Purpose

Use-case classes in this folder coordinate domain operations while keeping CLI and MCP thin.

## Main components

- `spec_service.py` (`SpecUseCase`): spec-level workflows (`new`, `validate`, `render`, `inspect`, `status`, `export`, `schema`, `templates`, `migrate`).
- `project_service.py` (`ProjectUseCase`): project-level workflows (`check`, `config get/set`).
- `feed_service.py` (`FeedUseCase`): multi-spec feed and sitemap workflows.
- `render_use_case.py` (`RenderUseCase`): batch project rendering.
- `project_context.py`: shared root/config discovery object.
- `filesystem.py`: side-effect gateway for filesystem operations.
- `dtos.py`: typed payload contracts returned by use cases.

## Rule

Callers (CLI/MCP) should import this layer instead of orchestrating domain internals directly.
