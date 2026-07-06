from typing import Literal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from config.main_settings import SETTINGS
from database.models.post import ContentMode, Post
from database.schema.content_blocks import parse_blocks_content
from database.schema.posts import PostCreate, PostDetailSchema, PostUpdate
from repositories import category_repo, post_repo, tag_repo, user_repo
from utils.content_renderer import render_post_content
from utils.slug_utils import normalize_slug


def _validate_blocks_content(content: str) -> None:
    try:
        parse_blocks_content(content)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


def _render_content(content_mode: ContentMode, content: str) -> str:
    try:
        return render_post_content(
            content_mode,
            content,
            use_node_ssr=SETTINGS.USE_NODE_SSR,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc


def _get_post_or_404(db: Session, post_id: int) -> Post:
    post = post_repo.get_by_id(db, post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post


def _validate_post_relations(
    db: Session,
    *,
    category_id: int | None,
    tag_ids: list[int] | None,
) -> None:
    if category_id is not None and category_repo.get_by_id(db, category_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    if tag_ids is None:
        return

    missing_tag_ids = [
        tag_id for tag_id in dict.fromkeys(tag_ids) if tag_repo.get_by_id(db, tag_id) is None
    ]
    if missing_tag_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag not found: {missing_tag_ids[0]}",
        )


def list_posts(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    *,
    sort: Literal["asc", "desc"] = "desc",
) -> list[Post]:
    return post_repo.get_all_with_author(db, skip=skip, limit=limit, sort=sort)


def get_post(db: Session, post_id: int) -> Post:
    post = post_repo.get_by_id_with_author(db, post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post


def get_post_by_slug(db: Session, slug: str) -> Post:
    post = post_repo.get_by_slug_with_author(db, slug)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post


def get_post_detail(db: Session, post_id: int) -> PostDetailSchema:
    post = post_repo.get_by_id_with_detail(db, post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return PostDetailSchema.model_validate(post)


def get_post_detail_by_slug(db: Session, slug: str) -> PostDetailSchema:
    post = post_repo.get_by_slug_with_detail(db, slug)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return PostDetailSchema.model_validate(post)


def create_post(db: Session, payload: PostCreate) -> Post:
    normalized_payload = payload.model_copy(
        update={"slug": normalize_slug(payload.slug or payload.title)}
    )

    if user_repo.get_by_id(db, normalized_payload.author_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found",
        )

    _validate_post_relations(
        db,
        category_id=normalized_payload.category_id,
        tag_ids=normalized_payload.tag_ids,
    )

    if (
        post_repo.get_by_slug(db, normalized_payload.slug, include_deleted=True)
        is not None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post slug already exists",
        )

    return post_repo.create(
        db,
        normalized_payload,
        rendered_content=_render_content(
            normalized_payload.content_mode,
            normalized_payload.content,
        ),
    )


def update_post(db: Session, post_id: int, payload: PostUpdate) -> Post:
    db_post = _get_post_or_404(db, post_id)
    update_payload = payload

    _validate_post_relations(
        db,
        category_id=payload.category_id,
        tag_ids=payload.tag_ids,
    )

    if payload.slug is not None:
        normalized_slug = normalize_slug(payload.slug)
        update_payload = payload.model_copy(update={"slug": normalized_slug})
        existing_post = post_repo.get_by_slug(
            db,
            normalized_slug,
            include_deleted=True,
        )
        if existing_post is not None and existing_post.id != post_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Post slug already exists",
            )

    effective_mode = (
        update_payload.content_mode
        if update_payload.content_mode is not None
        else db_post.content_mode
    )
    effective_content = (
        update_payload.content
        if update_payload.content is not None
        else db_post.content
    )

    if update_payload.content is not None and effective_mode == ContentMode.blocks:
        _validate_blocks_content(update_payload.content)

    rendered_content = None
    if update_payload.content is not None or update_payload.content_mode is not None:
        rendered_content = _render_content(effective_mode, effective_content)

    return post_repo.update(
        db,
        db_post,
        update_payload,
        rendered_content=rendered_content,
    )


def delete_post(db: Session, post_id: int) -> Post:
    db_post = _get_post_or_404(db, post_id)
    return post_repo.delete(db, db_post)
