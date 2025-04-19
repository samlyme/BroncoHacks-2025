from fastapi import APIRouter, HTTPException
from sqlmodel import select
from rag.db import SessionDep
from rag.models import Resource

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
