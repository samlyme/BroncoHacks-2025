from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

connection_string = f"postgresql://localhost:5432/samly"

engine = create_engine(connection_string)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
