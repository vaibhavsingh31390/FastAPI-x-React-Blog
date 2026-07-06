from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    display_name: str = Field(..., min_length=1, max_length=100)
    bio: str | None = Field(default=None, max_length=500)
    avatar_url: str | None = Field(default=None, max_length=255)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    display_name: str | None = Field(default=None, min_length=1, max_length=100)
    bio: str | None = Field(default=None, max_length=500)
    avatar_url: str | None = Field(default=None, max_length=255)


class UserAdminUpdate(BaseModel):
    is_active: bool | None = None
    is_admin: bool | None = None


class UsersSchema(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UsersSchema


class UserPublicSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    display_name: str
    avatar_url: str | None = None


class UserPostSummarySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    excerpt: str | None = None
    published_at: datetime | None = None


class UserWithPosts(UsersSchema):
    posts: list[UserPostSummarySchema] = Field(default_factory=list)


class UserCommentSummarySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    post_id: int
    parent_id: int | None = None
    author_name: str | None = None
    body: str
    created_at: datetime


class UserWithComments(UsersSchema):
    comments: list[UserCommentSummarySchema] = Field(default_factory=list)


class UserWithDetail(UsersSchema):
    posts: list[UserPostSummarySchema] = Field(default_factory=list)
    comments: list[UserCommentSummarySchema] = Field(default_factory=list)
