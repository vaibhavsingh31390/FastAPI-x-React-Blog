from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from database.schema.users import UserPublicSchema


class CommentBase(BaseModel):
    post_id: int = Field(..., gt=0)
    parent_id: int | None = Field(default=None, gt=0)
    author_name: str | None = Field(default=None, min_length=1, max_length=100)
    body: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    pass


class CommentAdminCreate(CommentBase):
    author_id: int | None = Field(default=None, gt=0)
    is_approved: bool = False


class CommentUpdate(BaseModel):
    parent_id: int | None = Field(default=None, gt=0)
    author_name: str | None = Field(default=None, min_length=1, max_length=100)
    body: str | None = Field(default=None, min_length=1)


class CommentAdminUpdate(CommentUpdate):
    author_id: int | None = Field(default=None, gt=0)
    is_approved: bool | None = None


# Internal / admin view: includes author_id, is_approved, all fields.
class CommentSchema(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int | None = None
    is_approved: bool
    created_at: datetime


# Public view: omits author_id and is_approved.
class CommentPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    post_id: int
    parent_id: int | None = None
    author_name: str | None = None
    body: str
    created_at: datetime


class CommentWithAuthorSchema(CommentPublicSchema):
    author: UserPublicSchema | None = None


class CommentDetailSchema(CommentWithAuthorSchema):
    replies: list[CommentWithAuthorSchema] = Field(default_factory=list)
