from typing import Literal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from database.models.category import Category
from database.schema.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryWithPostsSchema,
)
from repositories import category_repo
from utils.slug_utils import normalize_slug


def _get_category_or_404(db: Session, category_id: int) -> Category:
    category = category_repo.get_by_id(db, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category


def list_categories(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    *,
    sort: Literal["asc", "desc"] = "desc",
) -> list[Category]:
    return category_repo.get_all(db, skip=skip, limit=limit, sort=sort)


def get_category(db: Session, category_id: int) -> Category:
    return _get_category_or_404(db, category_id)


def get_category_by_slug(db: Session, slug: str) -> Category:
    category = category_repo.get_by_slug(db, slug)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category


def get_category_with_posts(db: Session, category_id: int) -> CategoryWithPostsSchema:
    category = category_repo.get_by_id_with_posts(db, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return CategoryWithPostsSchema.model_validate(category)


def get_category_with_posts_by_slug(
    db: Session,
    slug: str,
) -> CategoryWithPostsSchema:
    category = category_repo.get_by_slug_with_posts(db, slug)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return CategoryWithPostsSchema.model_validate(category)


def create_category(db: Session, payload: CategoryCreate) -> Category:
    normalized_payload = payload.model_copy(
        update={"slug": normalize_slug(payload.slug)}
    )

    if category_repo.get_by_slug(db, normalized_payload.slug) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category slug already exists",
        )
    return category_repo.create(db, normalized_payload)


def update_category(db: Session, category_id: int, payload: CategoryUpdate) -> Category:
    db_category = _get_category_or_404(db, category_id)
    update_payload = payload

    if payload.slug is not None:
        normalized_slug = normalize_slug(payload.slug)
        update_payload = payload.model_copy(update={"slug": normalized_slug})
        existing_category = category_repo.get_by_slug(db, normalized_slug)
        if existing_category is not None and existing_category.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category slug already exists",
            )

    return category_repo.update(db, db_category, update_payload)


def delete_category(db: Session, category_id: int) -> Category:
    db_category = _get_category_or_404(db, category_id)
    return category_repo.delete(db, db_category)
