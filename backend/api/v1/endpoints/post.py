from typing import Literal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from config.main_db import get_db
from database.schema.posts import (
    PostAdminSchema,
    PostCreate,
    PostDetailSchema,
    PostSchema,
    PostUpdate,
    PostWithAuthorSchema,
)
from services import post_service


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[PostWithAuthorSchema])
def list_posts(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    sort: Literal["asc", "desc"] = Query(default="desc"),
    db: Session = Depends(get_db),
):
    return post_service.list_posts(db, skip=skip, limit=limit, sort=sort)


@router.get("/{post_id}", response_model=PostWithAuthorSchema)
def get_post(post_id: int, db: Session = Depends(get_db)):
    return post_service.get_post(db, post_id)


@router.get("/{post_id}/detail", response_model=PostDetailSchema)
def get_post_detail(post_id: int, db: Session = Depends(get_db)):
    return post_service.get_post_detail(db, post_id)


@router.get("/slug/{slug}", response_model=PostWithAuthorSchema)
def get_post_by_slug(slug: str, db: Session = Depends(get_db)):
    return post_service.get_post_by_slug(db, slug)


@router.get("/slug/{slug}/detail", response_model=PostDetailSchema)
def get_post_detail_by_slug(slug: str, db: Session = Depends(get_db)):
    return post_service.get_post_detail_by_slug(db, slug)


# TODO: Protect this route with auth middleware and set `payload.author_id`
# from the authenticated user instead of trusting the request body.
@router.post("/", response_model=PostSchema, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate, db: Session = Depends(get_db)):
    return post_service.create_post(db, payload)


# TODO: Protect this route with auth middleware and verify the caller
# owns the post or has admin/editor permissions before allowing updates.
@router.patch("/{post_id}", response_model=PostSchema)
def update_post(
    post_id: int,
    payload: PostUpdate,
    db: Session = Depends(get_db),
):
    return post_service.update_post(db, post_id, payload)


# TODO: Protect this route with auth middleware and verify the caller
# owns the post or has admin/editor permissions before allowing deletes.
@router.delete("/{post_id}", response_model=PostAdminSchema)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    return post_service.delete_post(db, post_id)
