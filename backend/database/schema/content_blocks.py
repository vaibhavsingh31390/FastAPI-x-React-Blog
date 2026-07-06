import json
from typing import Any

from pydantic import BaseModel, Field, field_validator

ALLOWED_BLOCK_TYPES = frozenset({"heading", "paragraph", "cta", "image"})


class ContentBlock(BaseModel):
    type: str
    props: dict[str, Any] = Field(default_factory=dict)

    @field_validator("type")
    @classmethod
    def validate_type(cls, value: str) -> str:
        if value not in ALLOWED_BLOCK_TYPES:
            allowed = ", ".join(sorted(ALLOWED_BLOCK_TYPES))
            raise ValueError(f"Unsupported block type '{value}'. Allowed: {allowed}")
        return value


def parse_blocks_content(content: str) -> list[ContentBlock]:
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError("Blocks content must be valid JSON") from exc

    if not isinstance(data, list):
        raise ValueError("Blocks content must be a JSON array")

    return [ContentBlock.model_validate(block) for block in data]
