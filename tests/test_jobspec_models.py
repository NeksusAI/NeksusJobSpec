from __future__ import annotations

import pytest
from pydantic import ValidationError

from neksus.core.jobspec.models import JobSpec


def test_jobspec_model_rejects_invalid_id() -> None:
    with pytest.raises(ValidationError):
        JobSpec(
            schema_version=1,
            id="Backend Engineer",
            title="Backend Engineer",
            summary="Summary",
            responsibilities=["One"],
            requirements=["One"],
        )


def test_jobspec_model_rejects_empty_requirements() -> None:
    with pytest.raises(ValidationError):
        JobSpec(
            schema_version=1,
            id="backend-engineer",
            title="Backend Engineer",
            summary="Summary",
            responsibilities=["One"],
            requirements=[],
        )
