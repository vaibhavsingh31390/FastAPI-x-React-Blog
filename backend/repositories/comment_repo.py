from sqlalchemy.orm import Session, selectinload

from database.models.comment import Comment
from database.schema.comments import CommentCreate, CommentUpdate


def get_by_id(db: Session, comment_id: int) -> Comment | None:
    return db.query(Comment).filter(Comment.id == comment_id).first()


def get_by_post_id(
    db: Session,
    post_id: int,
    *,
    approved_only: bool = False,
) -> list[Comment]:
    query = db.query(Comment).filter(Comment.post_id == post_id)
    if approved_only:
        query = query.filter(Comment.is_approved.is_(True))
    return query.order_by(Comment.created_at.asc()).all()


def create(
    db: Session,
    comment_in: CommentCreate,
    *,
    author_id: int | None = None,
    is_approved: bool = False,
) -> Comment:
    db_comment = Comment(
        post_id=comment_in.post_id,
        parent_id=comment_in.parent_id,
        author_id=author_id,
        author_name=comment_in.author_name,
        body=comment_in.body,
        is_approved=is_approved,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def update(
    db: Session,
    db_comment: Comment,
    comment_in: CommentUpdate,
) -> Comment:
    update_data = comment_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_comment, field, value)

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def set_approved(db: Session, db_comment: Comment, *, is_approved: bool) -> Comment:
    db_comment.is_approved = is_approved
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete(db: Session, db_comment: Comment) -> Comment:
    db.delete(db_comment)
    db.commit()
    return db_comment


def get_all(
    db: Session,
    *,
    approved_only: bool | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Comment]:
    query = db.query(Comment).options(
        selectinload(Comment.author),
        selectinload(Comment.post),
    )
    if approved_only is True:
        query = query.filter(Comment.is_approved.is_(True))
    elif approved_only is False:
        query = query.filter(Comment.is_approved.is_(False))

    return query.order_by(Comment.created_at.desc()).offset(skip).limit(limit).all()
