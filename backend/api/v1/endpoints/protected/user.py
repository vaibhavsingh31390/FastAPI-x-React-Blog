from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.main_db import get_db
from database.schema.users import (
    UserUpdate,
    UserWithComments,
    UserWithDetail,
    UserWithPosts,
    UsersSchema,
)
from services import user_service

# Add dependencies=[Depends(get_current_user)] when auth middleware is ready.
router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}/posts", response_model=UserWithPosts)
def get_user_with_posts(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_with_posts(db, user_id)


@router.get("/{user_id}/comments", response_model=UserWithComments)
def get_user_with_comments(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_with_comments(db, user_id)


@router.get("/{user_id}/detail", response_model=UserWithDetail)
def get_user_detail(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_detail(db, user_id)


@router.patch("/{user_id}", response_model=UsersSchema)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
):
    return user_service.update_user(db, user_id, payload)


@router.delete("/{user_id}", response_model=UsersSchema)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.delete_user(db, user_id)
