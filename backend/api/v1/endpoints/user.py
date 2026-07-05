from typing import Literal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from config.main_db import get_db
from database.schema.users import (
    UserAdminUpdate,
    UserCreate,
    UserPublicSchema,
    UserUpdate,
    UserWithComments,
    UserWithDetail,
    UserWithPosts,
    UsersSchema,
)
from services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UsersSchema, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    return user_service.register(db, payload)


# TODO: Protect this route with auth middleware if you do not want the
# full user list exposed publicly. In most apps this is admin-only.
@router.get("/", response_model=list[UsersSchema])
def list_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    sort: Literal["asc", "desc"] = Query(default="desc"),
    db: Session = Depends(get_db),
):
    return user_service.list_users(db, skip=skip, limit=limit, sort=sort)


# TODO: Protect this route with auth middleware if user account fields
# like email, is_active, and is_admin should not be public.
@router.get("/{user_id}", response_model=UsersSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user(db, user_id)


@router.get("/{user_id}/public", response_model=UserPublicSchema)
def get_user_public_profile(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_public_profile(db, user_id)


# TODO: Protect this route with auth middleware if post history should
# only be visible to the user themself or to admins.
@router.get("/{user_id}/posts", response_model=UserWithPosts)
def get_user_with_posts(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_with_posts(db, user_id)


# TODO: Protect this route with auth middleware if comment history should
# only be visible to the user themself or to admins.
@router.get("/{user_id}/comments", response_model=UserWithComments)
def get_user_with_comments(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_with_comments(db, user_id)


# TODO: Protect this route with auth middleware if the combined user
# detail payload should not be public.
@router.get("/{user_id}/detail", response_model=UserWithDetail)
def get_user_detail(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_detail(db, user_id)


# TODO: Protect this route with auth middleware and verify the caller is
# updating their own account unless they have admin permissions.
@router.patch("/{user_id}", response_model=UsersSchema)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
):
    return user_service.update_user(db, user_id, payload)


# TODO: Protect this route with admin-only auth middleware.
@router.patch("/{user_id}/admin", response_model=UsersSchema)
def update_user_admin(
    user_id: int,
    payload: UserAdminUpdate,
    db: Session = Depends(get_db),
):
    return user_service.update_user_admin(db, user_id, payload)


# TODO: Protect this route with auth middleware and verify the caller is
# deleting their own account unless they have admin permissions.
@router.delete("/{user_id}", response_model=UsersSchema)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.delete_user(db, user_id)
