import json
from typing import Any

from pydantic import BaseModel, Field


class ContentComponent(BaseModel):
    name: str = Field(..., min_length=1)
    data: dict[str, Any] = Field(default_factory=dict)


def parse_components_content(content: str) -> list[ContentComponent]:
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError("Components content must be valid JSON") from exc

    if not isinstance(data, list):
        raise ValueError("Components content must be a JSON array")

    return [ContentComponent.model_validate(component) for component in data]
