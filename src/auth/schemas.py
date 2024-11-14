from pydantic import BaseModel, EmailStr
from sqlmodel import Field

from uuid import UUID
from datetime import datetime


class UserModel(BaseModel):
    uid: UUID
    username: str
    email: EmailStr
    password: str = Field(exclude=True)
    profile_picture: str
    bio: str
    created_at: datetime
    updated_at: datetime
    # posts:list[Post] will add after post features is make
    followers: list["UserModel"]
    following: list["UserModel"]


class UserCreateModel(BaseModel):
    username: str
    email: EmailStr
    password: str
    profile_picture: str
    bio: str


class UserUpdateModel(BaseModel):
    username: str | None = None
    password: str | None = None
    profile_picture: str | None = None
    bio: str | None = None
