from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base
from db.models.post import post_tags


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False)

    posts = relationship("Post", secondary=post_tags, back_populates="tags")