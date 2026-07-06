from typing import Literal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from api.dependencies.auth import get_current_user_optional
from config.main_db import get_db
from database.models.users import User
from database.schema.comments import CommentCreate, CommentWithAuthorSchema
from database.schema.posts import (
    CommentCreatePayload,
    PostDetailSchema,
    PostWithAuthorSchema,
)
from services import comment_service, post_service

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[PostWithAuthorSchema])
def list_posts(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    sort: Literal["asc", "desc"] = Query(default="desc"),
    db: Session = Depends(get_db),
):
    return post_service.list_published_posts(db, skip=skip, limit=limit, sort=sort)


@router.get("/{post_id}", response_model=PostWithAuthorSchema)
def get_post(post_id: int, db: Session = Depends(get_db)):
    return post_service.get_published_post(db, post_id)


@router.get("/{post_id}/detail", response_model=PostDetailSchema)
def get_post_detail(post_id: int, db: Session = Depends(get_db)):
    return post_service.get_published_post_detail(db, post_id)


@router.get("/slug/{slug}", response_model=PostWithAuthorSchema)
def get_post_by_slug(slug: str, db: Session = Depends(get_db)):
    return post_service.get_published_post_by_slug(db, slug)


@router.get("/slug/{slug}/detail", response_model=PostDetailSchema)
def get_post_detail_by_slug(slug: str, db: Session = Depends(get_db)):
    return post_service.get_published_post_detail_by_slug(db, slug)


@router.post(
    "/{post_id}/comments",
    response_model=CommentWithAuthorSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_post_comment(
    post_id: int,
    payload: CommentCreatePayload,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    return comment_service.create_comment(
        db,
        post_id,
        CommentCreate(
            post_id=post_id,
            parent_id=payload.parent_id,
            author_name=payload.author_name,
            body=payload.body,
        ),
        current_user=current_user,
    )
