from __future__ import annotations

import pytest
from pydantic import ValidationError

from neksus.core.jobspec.models import JobSpec


def test_jobspec_model_rejects_invalid_id() -> None:
    with pytest.raises(ValidationError):
        JobSpec.model_validate(
            {
                "schema_version": 1,
                "id": "Backend Engineer",
                "page": {"layout": "job_detail"},
                "job": {"title": "Backend Engineer"},
                "components": [
                    {
                        "type": "list",
                        "id": "requirements",
                        "variant": "bullets",
                        "title": "Requirements",
                        "items": ["One"],
                    }
                ],
            }
        )


def test_jobspec_model_rejects_empty_requirements_component() -> None:
    with pytest.raises(ValidationError):
        JobSpec.model_validate(
            {
                "schema_version": 1,
                "id": "backend-engineer",
                "page": {"layout": "job_detail"},
                "job": {"title": "Backend Engineer"},
                "components": [
                    {
                        "type": "list",
                        "id": "requirements",
                        "variant": "bullets",
                        "title": "Requirements",
                        "items": [],
                    }
                ],
            }
        )
