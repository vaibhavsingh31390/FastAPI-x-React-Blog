from typing import Literal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from database.models.users import User
from database.schema.users import (
    UserAdminUpdate,
    UserCreate,
    UserUpdate,
    UserPublicSchema,
    UserWithComments,
    UserWithPosts,
    UserWithDetail,
)
from repositories import user_repo


def _get_user_or_404(db: Session, user_id: int) -> User:
    user = user_repo.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


def list_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    *,
    sort: Literal["asc", "desc"] = "desc",
) -> list[User]:
    return user_repo.get_all(db, skip=skip, limit=limit, sort=sort)


def get_user(db: Session, user_id: int) -> User:
    return _get_user_or_404(db, user_id)


def get_user_by_email(db: Session, email: str) -> User | None:
    return user_repo.get_by_email(db, email)


def get_user_public_profile(db: Session, user_id: int) -> UserPublicSchema:
    return UserPublicSchema.model_validate(_get_user_or_404(db, user_id))


def get_user_with_posts(db: Session, user_id: int) -> UserWithPosts:
    return UserWithPosts.model_validate(_get_user_or_404(db, user_id))


def get_user_with_comments(db: Session, user_id: int) -> UserWithComments:
    return UserWithComments.model_validate(_get_user_or_404(db, user_id))


def get_user_detail(db: Session, user_id: int) -> UserWithDetail:
    return UserWithDetail.model_validate(_get_user_or_404(db, user_id))


def register(db: Session, payload: UserCreate) -> User:
    existing_user = user_repo.get_by_email(db, payload.email)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return user_repo.create(db, payload)


def update_user(db: Session, user_id: int, payload: UserUpdate) -> User:
    db_user = _get_user_or_404(db, user_id)

    if payload.email is not None:
        existing_user = user_repo.get_by_email(db, payload.email)
        if existing_user is not None and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    return user_repo.update(db, db_user, payload)


def update_user_admin(db: Session, user_id: int, payload: UserAdminUpdate) -> User:
    db_user = _get_user_or_404(db, user_id)
    return user_repo.update_admin(db, db_user, payload)


def delete_user(db: Session, user_id: int) -> User:
    db_user = _get_user_or_404(db, user_id)
    return user_repo.delete(db, db_user)
