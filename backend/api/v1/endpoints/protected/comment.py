from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies.auth import get_current_user
from config.main_db import get_db
from database.models.users import User
from database.schema.comments import CommentSchema, CommentUpdate, CommentWithAuthorSchema
from services import comment_service

router = APIRouter(prefix="/comments", tags=["comments"])


@router.patch("/{comment_id}", response_model=CommentWithAuthorSchema)
def update_comment(
    comment_id: int,
    payload: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return comment_service.update_comment(
        db,
        comment_id,
        payload,
        current_user=current_user,
    )


@router.delete("/{comment_id}", response_model=CommentSchema)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return comment_service.delete_comment(
        db,
        comment_id,
        current_user=current_user,
    )
