import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import text
from sqlmodel import Session, create_engine

load_dotenv()
engine = create_engine(os.getenv("DATABASE_PUBLIC_URL") or "lmao")

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]