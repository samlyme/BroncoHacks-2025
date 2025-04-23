from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from pgvector.sqlalchemy import Vector
from typing import Any, Optional, List

class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    category: str
    chunks: List["Chunk"] = Relationship(back_populates="document", cascade_delete=True)

class Chunk(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    embedding: Any = Field(sa_column=Column(Vector(1536)))
    document_id: int = Field(foreign_key="document.id")
    document: Optional[Document] = Relationship(back_populates="chunks")
