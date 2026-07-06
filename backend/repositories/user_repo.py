from typing import Literal

from pwdlib import PasswordHash
from sqlalchemy.orm import Session, selectinload

from database.models.users import User
from database.schema.users import (
    UserAdminUpdate,
    UserCreate,
    UserUpdate,
    UserWithComments,
)

password_hasher = PasswordHash.recommended()


def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    *,
    sort: Literal["asc", "desc"] = "desc",
) -> list[User]:
    order = User.created_at.desc() if sort == "desc" else User.created_at.asc()

    return db.query(User).order_by(order).offset(skip).limit(limit).all()


def get_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create(db: Session, user_in: UserCreate) -> User:
    db_user = User(
        email=user_in.email,
        password_hash=password_hasher.hash(user_in.password),
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        display_name=user_in.display_name,
        bio=user_in.bio,
        avatar_url=user_in.avatar_url,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update(db: Session, db_user: User, user_in: UserUpdate) -> User:
    update_data = user_in.model_dump(exclude_unset=True)
    password = update_data.pop("password", None)

    if password:
        db_user.password_hash = password_hasher.hash(password)

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_admin(db: Session, db_user: User, admin_in: UserAdminUpdate) -> User:
    update_data = admin_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete(db: Session, db_user: User) -> User:
    db.delete(db_user)
    db.commit()
    return db_user


def get_by_id_with_posts(db: Session, user_id: int) -> User | None:
    return (
        db.query(User)
        .options(selectinload(User.posts))
        .filter(User.id == user_id)
        .first()
    )


def get_by_id_with_comments(db: Session, user_id: int) -> User | None:
    return (
        db.query(User)
        .options(selectinload(User.comments))
        .filter(User.id == user_id)
        .first()
    )


def get_by_id_with_detail(db: Session, user_id: int) -> User | None:
    return (
        db.query(User)
        .options(
            selectinload(User.posts),
            selectinload(User.comments),
        )
        .filter(User.id == user_id)
        .first()
    )
