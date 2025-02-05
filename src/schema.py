"""SQLModel schema for the API."""

import uuid
from datetime import datetime
from enum import Enum

from sqlmodel import JSON, Column, Field, Relationship, SQLModel


class UserBucketLink(SQLModel, table=True):
    """A link table between users and buckets."""

    bucket_id: uuid.UUID = Field(foreign_key="bucket.id", primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", primary_key=True)


class User(SQLModel, table=True):
    """A generic user model."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    firstname: str
    lastname: str
    username: str
    email: str
    hashed_password: str
    created_at: datetime = Field(default=datetime.now())
    buckets: list["Bucket"] = Relationship(
        back_populates="users", link_model=UserBucketLink
    )


class CreateUser(SQLModel):
    """A generic user model for creating."""

    firstname: str
    lastname: str
    username: str
    email: str
    password: str


class UserUpdate(SQLModel):
    """A generic item model for updating."""

    username: str | None = None
    email: str | None = None
    password: str | None = None
    firstname: str | None = None
    lastname: str | None = None


class UserPublic(SQLModel):
    """A generic user model for public view."""

    id: uuid.UUID
    username: str
    email: str
    firstname: str
    lastname: str
    created_at: datetime


class Bucket(SQLModel, table=True):
    """A generic Bucket model."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    description: str | None = Field(default=None)
    bookmark: bool = Field(default=False)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    owner_id: uuid.UUID
    users: list[User] = Relationship(
        back_populates="buckets", link_model=UserBucketLink
    )
    items: list["Item"] = Relationship(back_populates="bucket")


class CreateBucket(SQLModel):
    """A generic bucket model for creating."""

    title: str
    description: str


class BucketUpdate(SQLModel):
    """A generic bucket model for updating."""

    title: str | None = None
    description: str | None = None
    bookmark: bool | None = None


class BucketPublic(SQLModel):
    """A generic bucket model for public view."""

    id: uuid.UUID
    title: str
    description: str
    bookmark: bool
    created_at: datetime
    updated_at: datetime
    owner_id: uuid.UUID


class BucketPublicWithUsers(BucketPublic):
    """A generic bucket model for public view with users."""

    users: list[UserPublic]


class ItemType(str, Enum):
    """A enum for item types."""

    activity = "activity"
    media = "media"
    food = "food"


class Item(SQLModel, table=True):
    """A generic item model."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    description: str | None = Field(default=None)
    location: str | None = Field(default=None)
    item_type: ItemType
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    bucket_id: uuid.UUID = Field(foreign_key="bucket.id")
    bucket: Bucket = Relationship(back_populates="items")
    ratings: dict[str, float] = Field(default_factory=dict, sa_column=Column(JSON))
    comments: dict[str, str] = Field(default_factory=dict, sa_column=Column(JSON))
    complete: bool = Field(default=False)


class CreateItem(SQLModel):
    """A generic item model for creating."""

    title: str
    description: str | None = None
    location: str | None = None
    item_type: ItemType


class ItemUpdate(SQLModel):
    """A generic item model for updating."""

    title: str | None = None
    description: str | None = None
    location: str | None = None
    score: float | None = None
    comment: str | None = None
    complete: bool | None = None
