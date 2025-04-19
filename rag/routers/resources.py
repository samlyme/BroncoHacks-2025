from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Column, Field, SQLModel, Session, select
from pgvector.sqlalchemy import Vector
from rag.db import SessionDep, get_session


class Resource(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    file_path: str
    label: str | None = None
    type: str | None = None
    upload_date: str | None = None
    chunk_text: str
    metadata: dict | None = None

    # Custom SQLAlchemy column for vector
    embedding: list[float] = Field(
        sa_column=Column(Vector(1536))  # use pgvector Vector
    )


router = APIRouter(prefix="/resources", tags=["Resources"])

# --- CREATE ---


@router.post("/")
def create_resource(resource: Resource, session: SessionDep):
    session.add(resource)
    session.commit()
    session.refresh(resource)
    return resource

# --- READ ALL ---


@router.get("/")
def read_resources(session: SessionDep):
    return session.exec(select(Resource)).all()

# --- READ ONE ---


@router.get("/{resource_id}")
def read_resource(resource_id: int, session: SessionDep):
    resource = session.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

# --- UPDATE ---


@router.put("/{resource_id}")
def update_resource(resource_id: int, updated: Resource, session: SessionDep):
    db_resource = session.get(Resource, resource_id)
    if not db_resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    for k, v in updated.dict(exclude_unset=True).items():
        setattr(db_resource, k, v)

    session.add(db_resource)
    session.commit()
    session.refresh(db_resource)
    return db_resource

# --- DELETE ---


@router.delete("/{resource_id}")
def delete_resource(resource_id: int, session: SessionDep):
    resource = session.get(Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    session.delete(resource)
    session.commit()
    return {"ok": True}
