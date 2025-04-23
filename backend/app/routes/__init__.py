from fastapi import APIRouter


router = APIRouter(prefix="/documents")

@router.post("/")
async def create_document(document):
    return document

@router.get("/")
async def read_documents():
    return {"message": "welcome"}

@router.get("/{id}")
async def read_document(id: int):
    return {"doc": id}

@router.delete("/{id}")
async def delete_document(id: int):
    return {"deleted": id}
