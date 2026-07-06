from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.main_db import get_db
from database.schema.users import UserPublicSchema
from services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}/public", response_model=UserPublicSchema)
def get_user_public_profile(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_public_profile(db, user_id)
