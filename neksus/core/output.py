"""Output helpers for CLI and core modules."""

from __future__ import annotations

import json
from typing import Any


def to_json(data: dict[str, Any]) -> str:
    """Serialize a dictionary into stable pretty JSON."""
    return json.dumps(data, indent=2, sort_keys=True)
