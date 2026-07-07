from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from config.main_db import get_db
from database.schema.tags import TagSchema, TagWithPostsSchema
from services import tag_service

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=list[TagSchema])
def list_tags(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    sort: Literal["asc", "desc"] = Query(default="desc"),
    db: Session = Depends(get_db),
):
    return tag_service.list_tags(db, skip=skip, limit=limit, sort=sort)


@router.get("/{tag_id}", response_model=TagSchema)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    return tag_service.get_tag(db, tag_id)


@router.get("/slug/{slug}", response_model=TagSchema)
def get_tag_by_slug(slug: str, db: Session = Depends(get_db)):
    return tag_service.get_tag_by_slug(db, slug)


@router.get("/{tag_id}/posts", response_model=TagWithPostsSchema)
def get_tag_with_posts(tag_id: int, db: Session = Depends(get_db)):
    return tag_service.get_tag_with_posts(db, tag_id)


@router.get("/slug/{slug}/posts", response_model=TagWithPostsSchema)
def get_tag_with_posts_by_slug(slug: str, db: Session = Depends(get_db)):
    return tag_service.get_tag_with_posts_by_slug(db, slug)
