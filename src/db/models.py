from sqlmodel import (
    SQLModel,
    Column,
    TIMESTAMP,
    UUID,
    Field,
)
import uuid
import datetime


class User(SQLModel, table=True):
    uid: uuid.UUID = Field(sa_column=Column(UUID, default=uuid.uuid4, primary_key=True))
    fullName: str
    email: str = Field(unique=True)
    username: str
    bio: str
    hashedPassword: str = Field(exclude=True)
    profileUrl: str
    createdAt: datetime.datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            default=lambda: datetime.datetime.now(datetime.timezone.utc),
        )
    )
