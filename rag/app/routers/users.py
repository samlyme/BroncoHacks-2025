
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.db import SessionDep
from app.models import User, UserCreate


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=User)
async def create_user(user: UserCreate, session: SessionDep):
    db_user = User.model_validate(user)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get("/", response_model=list[User])
async def read_users(session: SessionDep):
    return session.exec(select(User)).all()


@router.get("/{user_id}", response_model=User)
async def read_user(user_id: str, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=User)
async def update_user(user_id: str, session: SessionDep):
    raise HTTPException(status_code=400, detail="Unsupported")


@router.delete("/{user_id}", response_model=User)
async def delete_user(user_id: str, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    return user
