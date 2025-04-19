from typing import Annotated, Any, Sequence
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, SQLModel, Session, create_engine, select

from rag.db import create_db_and_tables, SessionDep
from rag.routers import resources

app = FastAPI()
app.include_router(resources.router)


class TaskBase(SQLModel):
    name: str = Field(default="Task", index=True)
    description: str = Field(default="desc")


class Task(TaskBase, table=True):
    id: int = Field(default=None, primary_key=True)


class TaskPublic(TaskBase):
    id: int


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    name: str | None = None
    description: str | None = None


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get('/')
async def home():
    return {'message': 'welcome'}


@app.post('/tasks')
async def create_task(task: Task, session: SessionDep) -> Task:
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# prefer regular typing when possible
@app.get('/tasks/', response_model=list[TaskPublic])
async def get_tasks(session: SessionDep) -> Sequence[Task]:
    return session.exec(select(Task)).all()


@app.get('/tasks/{task_id}')
async def read_task(task_id: int, session: SessionDep) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return task


@app.patch('/tasks/{task_id}')
async def update_task(task_id: int, task: TaskUpdate, session: SessionDep) -> Task:
    task_db = session.get(Task, task_id)
    if not task_db:
        raise HTTPException(status_code=404, detail="task not found")
    task_data = task.model_dump(exclude_unset=True)
    task_db.sqlmodel_update(task_data)
    session.add(task_db)
    session.commit()
    session.refresh(task_db)
    return task_db


@app.delete('/tasks/{task_id}')
async def delete_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")

    session.delete(task)
    session.commit()
    return task
