import enum
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import relationship

from config.main_db import Base, utc_now


class PostStatus(str, enum.Enum):
    draft = "draft"
    published = "published"
    archived = "archived"


class PostType(str, enum.Enum):
    post = "post"
    page = "page"


class ContentMode(str, enum.Enum):
    markdown = "markdown"
    html = "html"
    blocks = "blocks"


# Pivot table for posts <-> tags. Defined here; tag model imports it.
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column(
        "post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    ),
)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    author_id = Column(
        Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    category_id = Column(
        Integer,
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    slug = Column(String(100), nullable=False, unique=True)
    title = Column(String(100), nullable=False)
    excerpt = Column(String(500), nullable=True)
    content = Column(Text, nullable=False)
    content_mode = Column(
        Enum(ContentMode, name="contentmode"),
        nullable=False,
        default=ContentMode.html,
    )
    rendered_content = Column(Text, nullable=True)
    cover_image_url = Column(String(255), nullable=True)
    status = Column(
        Enum(PostStatus, name="poststatus"), nullable=False, default=PostStatus.draft
    )
    post_type = Column(
        Enum(PostType, name="posttype"), nullable=False, default=PostType.post
    )
    published_at = Column(DateTime(timezone=True), nullable=True)
    meta_title = Column(String(70), nullable=True)
    meta_description = Column(String(160), nullable=True)
    canonical_url = Column(String(255), nullable=True)
    robots = Column(String(50), nullable=True, default="index,follow")
    og_image_url = Column(String(255), nullable=True)
    focus_keyword = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)
    author = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )


# "published posts, newest first" query
Index("idx_posts_published", Post.status, Post.published_at.desc())
