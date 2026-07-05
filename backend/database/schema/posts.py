from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from database.models.post import PostStatus
from database.schema.users import UserPublicSchema


class PostBase(BaseModel):
    slug: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=100)
    excerpt: str | None = Field(default=None, max_length=500)
    content: str = Field(..., min_length=1)
    cover_image_url: str | None = Field(default=None, max_length=255)
    status: PostStatus = PostStatus.draft
    published_at: datetime | None = None
    category_id: int | None = Field(default=None, gt=0)


class PostCreate(PostBase):
    tag_ids: list[int] = Field(default_factory=list)


class PostUpdate(BaseModel):
    slug: str | None = Field(default=None, min_length=1, max_length=100)
    title: str | None = Field(default=None, min_length=1, max_length=100)
    excerpt: str | None = Field(default=None, max_length=500)
    content: str | None = Field(default=None, min_length=1)
    cover_image_url: str | None = Field(default=None, max_length=255)
    status: PostStatus | None = None
    published_at: datetime | None = None
    category_id: int | None = Field(default=None, gt=0)
    tag_ids: list[int] | None = None


class PostSchema(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime


class PostAdminSchema(PostSchema):
    deleted_at: datetime | None = None


class PostCategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    name: str
    description: str | None = None


class PostTagSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    name: str


class PostCommentSummarySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    parent_id: int | None = None
    author_name: str | None = None
    body: str
    created_at: datetime
    author: UserPublicSchema | None = None


class PostWithAuthorSchema(PostSchema):
    author: UserPublicSchema | None = None


class PostDetailSchema(PostWithAuthorSchema):
    category: PostCategorySchema | None = None
    tags: list[PostTagSchema] = Field(default_factory=list)
    comments: list[PostCommentSummarySchema] = Field(default_factory=list)
