from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.db import SessionDep
from app.models import Chat, ChatCreate

router = APIRouter(prefix="/chats", tags=["Chats"])


@router.post("/", response_model=Chat)
async def create_chat(chat: ChatCreate, session: SessionDep):
    db_chat = Chat.model_validate(chat)

    session.add(db_chat)
    session.commit()
    session.refresh(db_chat)

    return db_chat


@router.get("/", response_model=list[Chat])
async def read_chats(session: SessionDep):
    return session.exec(select(Chat)).all()

# The discord bot only has access to the thread id


@router.get("/{thread_id}", response_model=Chat)
async def read_chat(thread_id: str, session: SessionDep):
    chat = session.get(Chat, thread_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


# not supported bc bot doesn't listen for it
@router.patch("/{thread_id}", response_model=Chat)
async def update_chat(thread_id: str, session: SessionDep):
    raise HTTPException(status_code=400, detail="Unsupported")


@router.delete("/{thread_id}", response_model=Chat)
async def delete_user(thread_id: str, session: SessionDep):
    chat = session.get(Chat, thread_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    session.delete(chat)
    session.commit()
    return chat
