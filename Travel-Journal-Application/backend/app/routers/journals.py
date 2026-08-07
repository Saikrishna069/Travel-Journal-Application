from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models import JournalEntry
from app.database import get_database, IN_MEMORY_JOURNALS
from bson import ObjectId
import shutil
import os
import uuid

router = APIRouter(prefix="/journals", tags=["Journals"])
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def create_journal(entry: JournalEntry):
    data = entry.model_dump(exclude=["id"])
    data["user_id"] = "public_user"
    entry_id = str(uuid.uuid4())
    
    try:
        db = get_database()
        data["_id"] = entry_id
        await db.journals.insert_one(data)
    except Exception:
        pass

    IN_MEMORY_JOURNALS.append({"_id": entry_id, **data})
    return {"id": entry_id, "message": "Journal created successfully"}

@router.get("/")
async def get_journals():
    try:
        db = get_database()
        cursor = db.journals.find()
        entries = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            entries.append(doc)
        if entries:
            return entries
    except Exception:
        pass
    return IN_MEMORY_JOURNALS

@router.delete("/{entry_id}")
async def delete_journal(entry_id: str):
    global IN_MEMORY_JOURNALS
    try:
        db = get_database()
        await db.journals.delete_one({"_id": ObjectId(entry_id)})
    except Exception:
        pass

    IN_MEMORY_JOURNALS = [j for j in IN_MEMORY_JOURNALS if j.get("_id") != entry_id]
    return {"message": "Deleted successfully"}

@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, f"public_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"image_url": f"/static/{os.path.basename(file_path)}"}
