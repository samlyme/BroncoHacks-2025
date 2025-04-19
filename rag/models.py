from datetime import datetime
from typing import Annotated
from sqlmodel import Column, Field, SQLModel
from pgvector.sqlalchemy import Vector


class ResourceBase(SQLModel):
    name: str
    file_path: str
    label: str | None = None
    type: str | None = None


class Resource(ResourceBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    upload_date: datetime | None = Field(default_factory=datetime.utcnow)


class ResourceCreate(ResourceBase):
    name: str
    file_path: str
    label: str | None = None
    type: str | None = None


class ResourceUpdate(SQLModel):
    name: str | None = None
    file_path: str | None = None
    label: str | None = None
    type: str | None = None


class Chunk(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    resource_id: int = Field(foreign_key="resource.id")  # FK to resource
    chunk_text: str
    embedding: Annotated[
        list[float],
        Field(sa_column=Column(Vector(1536)))  # Using pgvector for embeddings
    ]


class UserBase(SQLModel):
    name: str
    email: str
    student_id: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    name: str | None
    email: str | None
    student_id: str | None
