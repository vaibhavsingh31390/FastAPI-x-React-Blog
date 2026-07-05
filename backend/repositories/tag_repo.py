from typing import Literal

from sqlalchemy.orm import Session, selectinload

from database.models.tag import Tag
from database.schema.tags import TagCreate, TagUpdate


def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    *,
    sort: Literal["asc", "desc"] = "desc",
) -> list[Tag]:
    order = Tag.created_at.desc() if sort == "desc" else Tag.created_at.asc()
    return db.query(Tag).order_by(order).offset(skip).limit(limit).all()


def get_by_id(db: Session, tag_id: int) -> Tag | None:
    return db.query(Tag).filter(Tag.id == tag_id).first()


def get_by_slug(db: Session, slug: str) -> Tag | None:
    return db.query(Tag).filter(Tag.slug == slug).first()


def create(db: Session, tag_in: TagCreate) -> Tag:
    db_tag = Tag(
        slug=tag_in.slug,
        name=tag_in.name,
    )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def update(db: Session, db_tag: Tag, tag_in: TagUpdate) -> Tag:
    update_data = tag_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tag, field, value)

    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def delete(db: Session, db_tag: Tag) -> Tag:
    db.delete(db_tag)
    db.commit()
    return db_tag


def get_by_id_with_posts(db: Session, tag_id: int) -> Tag | None:
    return (
        db.query(Tag)
        .options(selectinload(Tag.posts))
        .filter(Tag.id == tag_id)
        .first()
    )


def get_by_slug_with_posts(db: Session, slug: str) -> Tag | None:
    return (
        db.query(Tag)
        .options(selectinload(Tag.posts))
        .filter(Tag.slug == slug)
        .first()
    )
