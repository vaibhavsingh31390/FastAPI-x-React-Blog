from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from config.main_db import Base, utc_now
from database.models.post import post_tags


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    slug = Column(String(100), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = Column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )
    posts = relationship("Post", secondary=post_tags, back_populates="tags")
