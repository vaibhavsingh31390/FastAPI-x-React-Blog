from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from config.main_db import get_db
from database.schema.comments import CommentSchema
from services import comment_service

router = APIRouter(prefix="/comments", tags=["comments"])


@router.get("/", response_model=list[CommentSchema])
def list_comments(
    approved: bool | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return comment_service.list_comments(
        db,
        approved_only=approved,
        skip=skip,
        limit=limit,
    )


@router.patch("/{comment_id}/approve", response_model=CommentSchema)
def approve_comment(comment_id: int, db: Session = Depends(get_db)):
    return comment_service.approve_comment(db, comment_id)
