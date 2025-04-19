from typing import Annotated, Any, Sequence
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, SQLModel, Session, create_engine, select

from app.db import create_db_and_tables
from app.routers import resources, users
from app.routers import chats
from app.routers import messages

app = FastAPI()
app.include_router(resources.router)
app.include_router(users.router)
app.include_router(chats.router)
app.include_router(messages.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get('/')
async def home():
    return {'message': 'welcome'}
