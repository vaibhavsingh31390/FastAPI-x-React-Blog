from typing import Literal

from sqlalchemy.orm import Session, selectinload, with_loader_criteria

from config.main_db import utc_now
from database.models.comment import Comment
from database.models.post import Post, PostStatus
from database.models.tag import Tag
from database.schema.posts import PostCreate, PostUpdate


def _published_filter(query, *, published_only: bool):
    if published_only:
        query = query.filter(
            Post.deleted_at.is_(None),
            Post.status == PostStatus.published,
        )
    else:
        query = query.filter(Post.deleted_at.is_(None))
    return query


def _post_detail_options(*, approved_comments_only: bool = False):
    options = [
        selectinload(Post.author),
        selectinload(Post.category),
        selectinload(Post.tags),
        selectinload(Post.comments).selectinload(Comment.author),
    ]
    if approved_comments_only:
        options.append(
            with_loader_criteria(Comment, Comment.is_approved.is_(True))
        )
    return options


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
    published_only: bool = False,
) -> list[Post]:
    order = Post.created_at.desc() if sort == "desc" else Post.created_at.asc()

    query = db.query(Post)
    query = _published_filter(query, published_only=published_only)
    return query.order_by(order).offset(skip).limit(limit).all()


def get_all_with_author(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    *,
    sort: Literal["asc", "desc"] = "desc",
    published_only: bool = False,
) -> list[Post]:
    order = Post.published_at.desc() if sort == "desc" else Post.published_at.asc()

    query = db.query(Post).options(selectinload(Post.author))
    query = _published_filter(query, published_only=published_only)
    return query.order_by(order).offset(skip).limit(limit).all()


def get_by_id(
    db: Session,
    post_id: int,
    *,
    include_deleted: bool = False,
    published_only: bool = False,
) -> Post | None:
    query = db.query(Post)
    if not include_deleted:
        query = query.filter(Post.deleted_at.is_(None))
    if published_only:
        query = query.filter(Post.status == PostStatus.published)
    return query.filter(Post.id == post_id).first()


def get_by_slug(
    db: Session,
    slug: str,
    *,
    include_deleted: bool = False,
    published_only: bool = False,
) -> Post | None:
    query = db.query(Post)
    if not include_deleted:
        query = query.filter(Post.deleted_at.is_(None))
    if published_only:
        query = query.filter(Post.status == PostStatus.published)
    return query.filter(Post.slug == slug).first()


def create(
    db: Session,
    post_in: PostCreate,
    *,
    rendered_content: str | None = None,
) -> Post:
    db_post = Post(
        author_id=post_in.author_id,
        slug=post_in.slug,
        title=post_in.title,
        excerpt=post_in.excerpt,
        content=post_in.content,
        content_mode=post_in.content_mode,
        rendered_content=rendered_content,
        cover_image_url=post_in.cover_image_url,
        status=post_in.status,
        post_type=post_in.post_type,
        published_at=post_in.published_at,
        category_id=post_in.category_id,
        meta_title=post_in.meta_title,
        meta_description=post_in.meta_description,
        canonical_url=post_in.canonical_url,
        robots=post_in.robots,
        og_image_url=post_in.og_image_url,
        focus_keyword=post_in.focus_keyword,
    )
    db_post.tags = _get_tags_by_ids(db, post_in.tag_ids)

    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update(
    db: Session,
    db_post: Post,
    post_in: PostUpdate,
    *,
    rendered_content: str | None = None,
    update_rendered_content: bool = False,
) -> Post:
    update_data = post_in.model_dump(exclude_unset=True)
    tag_ids = update_data.pop("tag_ids", None)

    for field, value in update_data.items():
        setattr(db_post, field, value)

    if update_rendered_content:
        db_post.rendered_content = rendered_content

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
    *,
    include_deleted: bool = False,
    published_only: bool = False,
) -> Post | None:
    query = db.query(Post).options(selectinload(Post.author))
    if not include_deleted:
        query = query.filter(Post.deleted_at.is_(None))
    if published_only:
        query = query.filter(Post.status == PostStatus.published)
    return query.filter(Post.id == post_id).first()


def get_by_slug_with_author(
    db: Session,
    slug: str,
    *,
    include_deleted: bool = False,
    published_only: bool = False,
) -> Post | None:
    query = db.query(Post).options(selectinload(Post.author))
    if not include_deleted:
        query = query.filter(Post.deleted_at.is_(None))
    if published_only:
        query = query.filter(Post.status == PostStatus.published)
    return query.filter(Post.slug == slug).first()


def get_by_id_with_detail(
    db: Session,
    post_id: int,
    *,
    include_deleted: bool = False,
    published_only: bool = False,
    approved_comments_only: bool = False,
) -> Post | None:
    query = db.query(Post).options(
        *_post_detail_options(approved_comments_only=approved_comments_only)
    )
    if not include_deleted:
        query = query.filter(Post.deleted_at.is_(None))
    if published_only:
        query = query.filter(Post.status == PostStatus.published)
    return query.filter(Post.id == post_id).first()


def get_by_slug_with_detail(
    db: Session,
    slug: str,
    *,
    include_deleted: bool = False,
    published_only: bool = False,
    approved_comments_only: bool = False,
) -> Post | None:
    query = db.query(Post).options(
        *_post_detail_options(approved_comments_only=approved_comments_only)
    )
    if not include_deleted:
        query = query.filter(Post.deleted_at.is_(None))
    if published_only:
        query = query.filter(Post.status == PostStatus.published)
    return query.filter(Post.slug == slug).first()
