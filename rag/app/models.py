from datetime import datetime
from typing import Annotated
from sqlmodel import BigInteger, Column, Field, SQLModel
from pgvector.sqlalchemy import Vector


class ResourceBase(SQLModel):
    name: str
    file_path: str
    label: str
    type: str


class Resource(ResourceBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.utcnow)


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(ResourceBase):
    name: str | None
    file_path: str | None
    label: str | None
    type: str | None


class UserBase(SQLModel):
    discord_id: str = Field(primary_key=True)


class User(UserBase, table=True):
    created_at: datetime | None = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    pass


class ChatBase(SQLModel):
    thread_id: str = Field(primary_key=True)


class Chat(ChatBase, table=True):
    created_at: datetime | None = Field(default_factory=datetime.utcnow)


class ChatCreate(ChatBase):
    pass


class MessageBase(SQLModel):
    user_id: str = Field(foreign_key="user.discord_id")
    chat_id: str = Field(default=None, foreign_key="chat.thread_id")
    content: str


class Message(MessageBase, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.utcnow)


class MessageCreate(MessageBase):
    pass
