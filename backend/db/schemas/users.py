from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    password: str = Field(required=True, min_length=8, max_length=100)
    first_name: str = Field(required=True, min_length=1, max_length=100)
    last_name: str = Field(required=True, min_length=1, max_length=100) 
    display_name: str = Field(required=True, min_length=1, max_length=100)
    bio: str = Field(required=False, min_length=0, max_length=500)
    avatar_url: str = Field(required=False, min_length=0, max_length=255)
    is_active: bool = Field(required=True, default=True)
    is_admin: bool = Field(required=True, default=False)
    created_at: datetime = Field(required=True, default=datetime.now())
    updated_at: datetime = Field(required=True, default=datetime.now())