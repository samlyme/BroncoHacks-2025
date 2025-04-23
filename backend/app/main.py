from fastapi import FastAPI
from sqlmodel import SQLModel
from app.db import engine

from app.routes import documents

app = FastAPI()
app.include_router(documents.router)

@app.get('/')
async def home():
    return {'message': 'welcome'}

@app.on_event("startup")
def on_startup():
    # Creates all tables based on the models defined
    SQLModel.metadata.create_all(engine)