from fastapi import APIRouter


router = APIRouter(prefix="/documents")
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.db import get_session  # assume you have this defined somewhere
from app.models import Document, Chunk

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/", response_model=Document)
def create_document(document: Document, session: Session = Depends(get_session)):
    session.add(document)
    session.commit()
    session.refresh(document)
    return document


@router.get("/", response_model=List[Document])
def read_documents(session: Session = Depends(get_session)):
    return session.exec(select(Document)).all()


@router.get("/{id}", response_model=Document)
def read_document(id: int, session: Session = Depends(get_session)):
    document = session.get(Document, id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/{id}")
def delete_document(id: int, session: Session = Depends(get_session)):
    document = session.get(Document, id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    session.delete(document)
    session.commit()
    return {"ok": True}
