import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Enum, ForeignKey, Index, Table,
)
from sqlalchemy.orm import relationship
from db.base import Base


class PostStatus(str, enum.Enum):
    draft = "draft"
    published = "published"
    archived = "archived"


# Pivot table for posts <-> tags. Defined here; tag model imports it.
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)
    slug = Column(String, nullable=False, unique=True, index=True)
    title = Column(String, nullable=False)
    excerpt = Column(Text, nullable=True)          # teaser / meta description
    content = Column(Text, nullable=False)         # markdown or html body
    cover_image_url = Column(String, nullable=True)
    status = Column(Enum(PostStatus), nullable=False, default=PostStatus.draft)
    published_at = Column(DateTime, nullable=True)  # set when published
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    author = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")


# "published posts, newest first" query
Index("idx_posts_published", Post.status, Post.published_at.desc())