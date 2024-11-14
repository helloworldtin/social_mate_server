from pydantic import BaseModel, Field
from src.auth.routes import UserModel

from datetime import datetime


class PostModel(BaseModel):
    uid: str
    title: str
    subtitle: str
    post_pictures: list[str]
    user: UserModel
    created_at: datetime
    updated_at: datetime


class PostCreateModel(BaseModel):
    title : str = Field(...,max_length=100)
    subtitle : str
    post_pictures: str
