from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from config.main_db import get_db
from database.schema.users import UserAdminUpdate, UsersSchema
from services import user_service

# Add dependencies=[Depends(get_current_admin)] when auth middleware is ready.
router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UsersSchema])
def list_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    sort: Literal["asc", "desc"] = Query(default="desc"),
    db: Session = Depends(get_db),
):
    return user_service.list_users(db, skip=skip, limit=limit, sort=sort)


@router.get("/{user_id}", response_model=UsersSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user(db, user_id)


@router.patch("/{user_id}/admin", response_model=UsersSchema)
def update_user_admin(
    user_id: int,
    payload: UserAdminUpdate,
    db: Session = Depends(get_db),
):
    return user_service.update_user_admin(db, user_id, payload)
