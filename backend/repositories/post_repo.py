from typing import Literal

from sqlalchemy.orm import Session, selectinload

from config.main_db import utc_now
from database.models.comment import Comment
from database.models.post import Post
from database.models.tag import Tag
from database.schema.posts import PostCreate, PostUpdate


def _get_tags_by_ids(db: Session, tag_ids: list[int]) -> list[Tag]:
    if not tag_ids:
        return []

    unique_tag_ids = list(dict.fromkeys(tag_ids))
    tags = db.query(Tag).filter(Tag.id.in_(unique_tag_ids)).all()
    tags_by_id = {tag.id: tag for tag in tags}
    return [tags_by_id[tag_id] for tag_id in unique_tag_ids if tag_id in tags_by_id]


def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    *,
    sort: Literal["asc", "desc"] = "desc",
) -> list[Post]:
    order = Post.created_at.desc() if sort == "desc" else Post.created_at.asc()

    return (
        db.query(Post)
        .filter(Post.deleted_at.is_(None))
        .order_by(order)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_all_with_author(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    *,
    sort: Literal["asc", "desc"] = "desc",
) -> list[Post]:
    order = Post.created_at.desc() if sort == "desc" else Post.created_at.asc()

    return (
        db.query(Post)
        .options(selectinload(Post.author))
        .filter(Post.deleted_at.is_(None))
        .order_by(order)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_by_id(db: Session, post_id: int, include_deleted: bool = False) -> Post | None:
    query = db.query(Post)
    if not include_deleted:
        query = query.filter(Post.deleted_at.is_(None))
    return query.filter(Post.id == post_id).first()


def get_by_slug(
    db: Session,
    slug: str,
    include_deleted: bool = False,
) -> Post | None:
    query = db.query(Post)
    if not include_deleted:
        query = query.filter(Post.deleted_at.is_(None))
    return query.filter(Post.slug == slug).first()


def create(db: Session, post_in: PostCreate) -> Post:
    db_post = Post(
        author_id=post_in.author_id,
        slug=post_in.slug,
        title=post_in.title,
        excerpt=post_in.excerpt,
        content=post_in.content,
        cover_image_url=post_in.cover_image_url,
        status=post_in.status,
        published_at=post_in.published_at,
        category_id=post_in.category_id,
    )
    db_post.tags = _get_tags_by_ids(db, post_in.tag_ids)

    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update(db: Session, db_post: Post, post_in: PostUpdate) -> Post:
    update_data = post_in.model_dump(exclude_unset=True)
    tag_ids = update_data.pop("tag_ids", None)

    for field, value in update_data.items():
        setattr(db_post, field, value)

    if tag_ids is not None:
        db_post.tags = _get_tags_by_ids(db, tag_ids)

    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete(db: Session, db_post: Post) -> Post:
    db_post.deleted_at = utc_now()
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_by_id_with_author(
    db: Session,
    post_id: int,
    include_deleted: bool = False,
) -> Post | None:
    query = db.query(Post).options(selectinload(Post.author))
    if not include_deleted:
        query = query.filter(Post.deleted_at.is_(None))
    return query.filter(Post.id == post_id).first()


def get_by_slug_with_author(
    db: Session,
    slug: str,
    include_deleted: bool = False,
) -> Post | None:
    query = db.query(Post).options(selectinload(Post.author))
    if not include_deleted:
        query = query.filter(Post.deleted_at.is_(None))
    return query.filter(Post.slug == slug).first()


def get_by_id_with_detail(
    db: Session,
    post_id: int,
    include_deleted: bool = False,
) -> Post | None:
    query = db.query(Post).options(
        selectinload(Post.author),
        selectinload(Post.category),
        selectinload(Post.tags),
        selectinload(Post.comments).selectinload(Comment.author),
    )
    if not include_deleted:
        query = query.filter(Post.deleted_at.is_(None))
    return query.filter(Post.id == post_id).first()


def get_by_slug_with_detail(
    db: Session,
    slug: str,
    include_deleted: bool = False,
) -> Post | None:
    query = db.query(Post).options(
        selectinload(Post.author),
        selectinload(Post.category),
        selectinload(Post.tags),
        selectinload(Post.comments).selectinload(Comment.author),
    )
    if not include_deleted:
        query = query.filter(Post.deleted_at.is_(None))
    return query.filter(Post.slug == slug).first()
