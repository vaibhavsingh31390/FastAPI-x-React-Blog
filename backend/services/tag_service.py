from typing import Literal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from database.models.post import PostStatus
from database.models.tag import Tag
from database.schema.tags import TagCreate, TagUpdate, TagWithPostsSchema
from repositories import tag_repo
from utils.slug_utils import normalize_slug


def _filter_published_posts(tag: Tag) -> None:
    tag.posts = [
        post
        for post in tag.posts
        if post.deleted_at is None and post.status == PostStatus.published
    ]


def _get_tag_or_404(db: Session, tag_id: int) -> Tag:
    tag = tag_repo.get_by_id(db, tag_id)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )
    return tag


def list_tags(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    *,
    sort: Literal["asc", "desc"] = "desc",
) -> list[Tag]:
    return tag_repo.get_all(db, skip=skip, limit=limit, sort=sort)


def get_tag(db: Session, tag_id: int) -> Tag:
    return _get_tag_or_404(db, tag_id)


def get_tag_by_slug(db: Session, slug: str) -> Tag:
    tag = tag_repo.get_by_slug(db, slug)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )
    return tag


def get_tag_with_posts(db: Session, tag_id: int) -> TagWithPostsSchema:
    tag = tag_repo.get_by_id_with_posts(db, tag_id)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )
    _filter_published_posts(tag)
    return TagWithPostsSchema.model_validate(tag)


def get_tag_with_posts_by_slug(db: Session, slug: str) -> TagWithPostsSchema:
    tag = tag_repo.get_by_slug_with_posts(db, slug)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )
    _filter_published_posts(tag)
    return TagWithPostsSchema.model_validate(tag)


def create_tag(db: Session, payload: TagCreate) -> Tag:
    normalized_payload = payload.model_copy(
        update={"slug": normalize_slug(payload.slug or payload.name)}
    )

    if tag_repo.get_by_slug(db, normalized_payload.slug) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag slug already exists",
        )
    return tag_repo.create(db, normalized_payload)


def update_tag(db: Session, tag_id: int, payload: TagUpdate) -> Tag:
    db_tag = _get_tag_or_404(db, tag_id)
    update_payload = payload

    if payload.slug is not None:
        normalized_slug = normalize_slug(payload.slug)
        update_payload = payload.model_copy(update={"slug": normalized_slug})
        existing_tag = tag_repo.get_by_slug(db, normalized_slug)
        if existing_tag is not None and existing_tag.id != tag_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tag slug already exists",
            )

    return tag_repo.update(db, db_tag, update_payload)


def delete_tag(db: Session, tag_id: int) -> Tag:
    db_tag = _get_tag_or_404(db, tag_id)
    return tag_repo.delete(db, db_tag)
