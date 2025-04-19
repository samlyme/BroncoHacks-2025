
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from rag.db import SessionDep
from rag.models import User, UserCreate, UserUpdate


router = APIRouter(prefix="/users", tags=["Users"])

# Create user

# Create user


@router.post("/", response_model=User)
def create_user(user: UserCreate, session: SessionDep):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Read all users


@router.get("/", response_model=list[User])
def read_users(session: SessionDep):
    return session.exec(select(User)).all()

# Read one user by ID


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update user


@router.patch("/{user_id}", response_model=User)
def update_user(user_id: int, updated: UserUpdate, session: SessionDep):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = updated.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

# Delete user


@router.delete("/{user_id}")
def delete_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    return {"ok": True}
