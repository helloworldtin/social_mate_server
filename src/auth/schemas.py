from pydantic import BaseModel
from sqlmodel import Field
from fastapi import Form

from uuid import UUID
from datetime import datetime


class UserModel(BaseModel):
    uid: UUID
    fullName: str
    email: str
    username: str
    bio: str
    hashedPassword: str = Field(exclude=True)
    profileUrl: str
    createdAt: datetime


class UserCreateModel(BaseModel):
    fullName: str
    email: str
    password: str
    bio: str
    # profileUrl: we are taking profile URL directly from the request


class LoginInModel(BaseModel):
    email: str
    password: str


class VerifyOTPModel(BaseModel):
    email: str
    OTP: str
