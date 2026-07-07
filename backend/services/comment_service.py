from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from database.models.comment import Comment
from database.models.users import User
from database.schema.comments import (
    CommentCreate,
    CommentSchema,
    CommentUpdate,
    CommentWithAuthorSchema,
)
from repositories import comment_repo, post_repo


def _comment_not_found() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Comment not found",
    )


def _get_comment_or_404(db: Session, comment_id: int) -> Comment:
    comment = comment_repo.get_by_id(db, comment_id)
    if comment is None:
        raise _comment_not_found()
    return comment


def _ensure_can_modify(comment: Comment, user: User) -> None:
    if user.is_admin:
        return
    if comment.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to modify this comment",
        )


def list_comments(
    db: Session,
    *,
    approved_only: bool | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Comment]:
    return comment_repo.get_all(
        db,
        approved_only=approved_only,
        skip=skip,
        limit=limit,
    )


def create_comment(
    db: Session,
    post_id: int,
    payload: CommentCreate,
    *,
    current_user: User | None = None,
) -> CommentWithAuthorSchema:
    post = post_repo.get_by_id(db, post_id, published_only=True)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if payload.parent_id is not None:
        parent = comment_repo.get_by_id(db, payload.parent_id)
        if parent is None or parent.post_id != post_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid parent comment",
            )

    author_id = current_user.id if current_user is not None else None
    author_name = payload.author_name
    if current_user is not None:
        author_name = author_name or current_user.display_name
    elif not author_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="author_name is required for guest comments",
        )

    comment = comment_repo.create(
        db,
        CommentCreate(
            post_id=post_id,
            parent_id=payload.parent_id,
            author_name=author_name,
            body=payload.body,
        ),
        author_id=author_id,
        is_approved=False,
    )
    return CommentWithAuthorSchema.model_validate(comment)


def update_comment(
    db: Session,
    comment_id: int,
    payload: CommentUpdate,
    *,
    current_user: User,
) -> CommentWithAuthorSchema:
    comment = _get_comment_or_404(db, comment_id)
    _ensure_can_modify(comment, current_user)
    updated = comment_repo.update(db, comment, payload)
    return CommentWithAuthorSchema.model_validate(updated)


def delete_comment(db: Session, comment_id: int, *, current_user: User) -> CommentSchema:
    comment = _get_comment_or_404(db, comment_id)
    _ensure_can_modify(comment, current_user)
    return CommentSchema.model_validate(comment_repo.delete(db, comment))


def approve_comment(db: Session, comment_id: int) -> CommentSchema:
    comment = _get_comment_or_404(db, comment_id)
    return CommentSchema.model_validate(
        comment_repo.set_approved(db, comment, is_approved=True)
    )
