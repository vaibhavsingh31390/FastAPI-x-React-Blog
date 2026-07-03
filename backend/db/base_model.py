# Base Class for the database models

from typing import Any
from sqlalchemy.orm import DeclarativeBase, declared_attr

class BaseModel(DeclarativeBase):
    id: Any
    __name__: str
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()