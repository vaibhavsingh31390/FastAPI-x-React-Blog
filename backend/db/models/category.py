from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from db.base import Base


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    posts = relationship("Post", back_populates="category")