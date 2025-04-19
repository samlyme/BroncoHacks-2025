from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.db import SessionDep
from app.models import Resource, ResourceCreate, ResourceUpdate

router = APIRouter(prefix="/rag", tags=["Rag"])
