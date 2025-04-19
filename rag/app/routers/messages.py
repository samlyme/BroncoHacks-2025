from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.db import SessionDep
from app.models import Message, MessageCreate

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/", response_model=Message)
async def create_message(message: MessageCreate, session: SessionDep):
    db_message = Message.model_validate(message)

    session.add(db_message)
    session.commit()
    session.refresh(db_message)

    return db_message


@router.get("/", response_model=list[Message])
async def get_messages(session: SessionDep):
    statement = select(Message)
    return session.exec(statement).all()
