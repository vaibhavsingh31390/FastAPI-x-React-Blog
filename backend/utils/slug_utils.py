from fastapi import HTTPException, status
from slugify import slugify


def normalize_slug(value: str) -> str:
    normalized = slugify(value)
    if not normalized:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slug must contain letters or numbers",
        )
    return normalized
