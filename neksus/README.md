# `neksus` Package

This package contains the full Neksus JobSpec implementation.

## Purpose

`neksus` is the installable Python package that exposes:
- the CLI entrypoint (`neksus-jobspec`)
- a reusable core library (`neksus.core`) for parsing, validating, rendering, and checking JobSpecs

## High-level layout

- `cli/`: Typer command layer (I/O, argument parsing, exit codes)
- `core/`: business logic and domain models (framework-independent)
- `__init__.py`: package version (`__version__`)
- `py.typed`: marker that this package ships typing information

## Design principles

- CLI stays thin and delegates to core.
- Core does not import CLI code.
- JSON output shapes are stable and testable.
- Exceptions are domain-specific and mapped to stable exit codes by CLI helpers.
