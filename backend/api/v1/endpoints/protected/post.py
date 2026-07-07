from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.main_db import get_db
from database.schema.posts import PostAdminSchema, PostCreate, PostSchema, PostUpdate
from services import post_service

# Add dependencies=[Depends(get_current_user)] when auth middleware is ready.
router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostSchema, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate, db: Session = Depends(get_db)):
    return post_service.create_post(db, payload)


@router.patch("/{post_id}", response_model=PostSchema)
def update_post(
    post_id: int,
    payload: PostUpdate,
    db: Session = Depends(get_db),
):
    return post_service.update_post(db, post_id, payload)


@router.delete("/{post_id}", response_model=PostAdminSchema)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    return post_service.delete_post(db, post_id)
