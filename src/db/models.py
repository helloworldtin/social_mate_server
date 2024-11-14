from sqlmodel import (
    SQLModel,
    Column,
    TIMESTAMP,
    JSON,
    UUID,
    String,
    Field,
    Relationship,
)
from pydantic import EmailStr

import uuid
import datetime


class UserFollow(SQLModel, table=True):
    user_uid: uuid.UUID = Field(
        foreign_key="users.uid", primary_key=True
    )  # this is the uid of followers
    followers_uid: uuid.UUID = Field(
        foreign_key="users.uid", primary_key=True
    )  # this is hte uid of the followed person


class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        sa_column=Column(UUID, primary_key=True, default=uuid.uuid4),
    )
    username: str
    email: EmailStr
    password: str = Field(exclude=True)
    profile_picture: str
    bio: str = Field(sa_column=Column(String, nullable=True))
    created_at: datetime.datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            default=datetime.datetime.now,
        )
    )
    posts: list["Post"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            default=datetime.datetime.now,
        )
    )
    followers: list["User"] = Relationship(
        back_populates="following",
        link_model=UserFollow,
        sa_relationship_kwargs={
            "lazy": "selectin",
            "foreign_keys": "[UserFollow.followers_uid]",
        },
    )
    following: list["User"] = Relationship(
        back_populates="followers",
        link_model=UserFollow,
        sa_relationship_kwargs={
            "lazy": "selectin",
            "foreign_keys": "[UserFollow.user_uid]",
            "cascade": "all",
        },
    )


class Post(SQLModel, table=True):
    __tablename__ = "posts"
    uid: uuid.UUID = Field(
        sa_column=Column(UUID, primary_key=True, default=uuid.uuid4),
    )
    title: str
    subtitle: str
    post_pictures: list[str] = Field(sa_column=Column(JSON))
    user: User = Relationship(back_populates="posts")
    user_uid: uuid.UUID = Field(foreign_key='users.uid')
    created_at: datetime.datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            default=datetime.datetime.now,
        )
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            default=datetime.datetime.now,
        )
    )
