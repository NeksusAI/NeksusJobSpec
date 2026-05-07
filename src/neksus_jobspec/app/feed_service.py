"""Application service for feed export and sitemap workflows."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from neksus_jobspec.errors import InvalidInputError, NeksusError
from neksus_jobspec.jobspec.feeds import (
    expand_input_paths,
    render_jobs_json_feed,
    render_jobs_xml_feed,
    render_sitemap,
)
from neksus_jobspec.jobspec.parser import load_jobspec


class FeedUseCase:
    """Use-case orchestration for feed and sitemap operations."""

    def export(
        self,
        *,
        inputs: list[str],
        target: str,
        out: Path,
        skip_invalid: bool = False,
    ) -> dict[str, Any]:
        """Export multiple JobSpecs into a deterministic jobs feed.

        Args:
            inputs: File paths, directory paths, or glob expressions.
            target: Export format target (`jobs-json` or `jobs-xml`).
            out: Destination output file path.
            skip_invalid: Whether invalid input files should be skipped.

        Returns:
            Payload containing output path, record count, and skipped inputs.

        Raises:
            InvalidInputError: If no input files are resolved or target is unsupported.
            NeksusError: If invalid inputs are found and `skip_invalid` is False.
        """
        paths = expand_input_paths(inputs)
        if not paths:
            raise InvalidInputError("No input files found.")
        specs = []
        invalid: list[str] = []
        for path in paths:
            try:
                specs.append(load_jobspec(path))
            except Exception:  # noqa: BLE001
                invalid.append(str(path))
        if invalid and not skip_invalid:
            raise NeksusError(f"Invalid JobSpec input(s): {', '.join(invalid)}")
        if target == "jobs-json":
            content = render_jobs_json_feed(specs)
        elif target == "jobs-xml":
            content = render_jobs_xml_feed(specs)
        else:
            raise InvalidInputError("Unsupported target. Use: jobs-json or jobs-xml")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
        return {
            "ok": True,
            "target": target,
            "output": str(out),
            "count": len(specs),
            "invalid": invalid,
        }

    def sitemap(
        self,
        *,
        inputs: list[str],
        base_url: str,
        out: Path,
        exclude_closed: bool = False,
    ) -> dict[str, Any]:
        """Generate a sitemap document from multiple JobSpec inputs.

        Args:
            inputs: File paths, directory paths, or glob expressions.
            base_url: Public base URL used for sitemap entry generation.
            out: Destination sitemap output file path.
            exclude_closed: Whether closed/expired specs are excluded.

        Returns:
            Payload containing output path and processed spec count.

        Raises:
            InvalidInputError: If no input files are resolved.
        """
        paths = expand_input_paths(inputs)
        if not paths:
            raise InvalidInputError("No input files found.")
        specs = [load_jobspec(path) for path in paths]
        content = render_sitemap(specs, base_url, exclude_closed=exclude_closed)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
        return {
            "ok": True,
            "output": str(out),
            "count": len(specs),
            "exclude_closed": exclude_closed,
        }
