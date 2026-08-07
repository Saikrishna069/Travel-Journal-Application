from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response
from app.models import JournalEntry
from app.database import get_database, IN_MEMORY_JOURNALS
from app.utils import get_current_user
from bson import ObjectId
import shutil
import os
import uuid

router = APIRouter(prefix="/journals", tags=["Journals"])
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def process_create_journal(entry: JournalEntry, user_id: str):
    data = entry.model_dump(exclude=["id"])
    data["user_id"] = user_id
    entry_id = str(uuid.uuid4())
    data["_id"] = entry_id
    
    try:
        db = get_database()
        await db.journals.insert_one(dict(data))
    except Exception:
        pass

    IN_MEMORY_JOURNALS.append(data)
    return {"id": entry_id, "message": "Journal created successfully"}

async def process_get_journals(user_id: str):
    try:
        db = get_database()
        cursor = db.journals.find({"user_id": user_id}).sort("created_at", 1)
        entries = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            entries.append(doc)
        if entries:
            return entries
    except Exception:
        pass

    return [j for j in IN_MEMORY_JOURNALS if j.get("user_id") == user_id]

@router.post("")
async def create_journal_no_slash(entry: JournalEntry, user_id: str = Depends(get_current_user)):
    return await process_create_journal(entry, user_id)

@router.post("/")
async def create_journal_with_slash(entry: JournalEntry, user_id: str = Depends(get_current_user)):
    return await process_create_journal(entry, user_id)

@router.options("")
@router.options("/")
async def options_journals():
    return Response(status_code=200)

@router.get("")
async def get_journals_no_slash(user_id: str = Depends(get_current_user)):
    return await process_get_journals(user_id)

@router.get("/")
async def get_journals_with_slash(user_id: str = Depends(get_current_user)):
    return await process_get_journals(user_id)

@router.delete("/{entry_id}")
@router.delete("/{entry_id}/")
async def delete_journal(entry_id: str, user_id: str = Depends(get_current_user)):
    global IN_MEMORY_JOURNALS
    try:
        db = get_database()
        await db.journals.delete_one({"_id": ObjectId(entry_id), "user_id": user_id})
    except Exception:
        pass

    IN_MEMORY_JOURNALS = [j for j in IN_MEMORY_JOURNALS if not (j.get("_id") == entry_id and j.get("user_id") == user_id)]
    return {"message": "Deleted successfully"}

@router.post("/upload-image")
@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...), user_id: str = Depends(get_current_user)):
    file_path = os.path.join(UPLOAD_DIR, f"{user_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"image_url": f"/static/{os.path.basename(file_path)}"}
