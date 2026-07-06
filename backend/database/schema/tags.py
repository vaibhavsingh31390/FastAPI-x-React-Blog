from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TagBase(BaseModel):
    slug: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=100)


class TagCreate(TagBase):
    slug: str | None = Field(default=None, min_length=1, max_length=100)


class TagUpdate(BaseModel):
    slug: str | None = Field(default=None, min_length=1, max_length=100)
    name: str | None = Field(default=None, min_length=1, max_length=100)


class TagSchema(TagBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class TagPostSummarySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    excerpt: str | None = None
    cover_image_url: str | None = None
    status: str
    published_at: datetime | None = None
    created_at: datetime


class TagWithPostsSchema(TagSchema):
    posts: list[TagPostSummarySchema] = Field(default_factory=list)
