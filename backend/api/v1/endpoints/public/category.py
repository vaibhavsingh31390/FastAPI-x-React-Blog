from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from config.main_db import get_db
from database.schema.category import CategorySchema, CategoryWithPostsSchema
from services import category_service

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategorySchema])
def list_categories(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    sort: Literal["asc", "desc"] = Query(default="desc"),
    db: Session = Depends(get_db),
):
    return category_service.list_categories(db, skip=skip, limit=limit, sort=sort)


@router.get("/{category_id}", response_model=CategorySchema)
def get_category(category_id: int, db: Session = Depends(get_db)):
    return category_service.get_category(db, category_id)


@router.get("/slug/{slug}", response_model=CategorySchema)
def get_category_by_slug(slug: str, db: Session = Depends(get_db)):
    return category_service.get_category_by_slug(db, slug)


@router.get("/{category_id}/posts", response_model=CategoryWithPostsSchema)
def get_category_with_posts(category_id: int, db: Session = Depends(get_db)):
    return category_service.get_category_with_posts(db, category_id)


@router.get("/slug/{slug}/posts", response_model=CategoryWithPostsSchema)
def get_category_with_posts_by_slug(slug: str, db: Session = Depends(get_db)):
    return category_service.get_category_with_posts_by_slug(db, slug)
