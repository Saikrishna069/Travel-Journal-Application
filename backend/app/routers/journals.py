from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.models import JournalEntry
from app.database import get_database
from app.utils import get_current_user
from bson import ObjectId
import shutil
import os

router = APIRouter(prefix="/journals", tags=["Journals"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def create_journal(entry: JournalEntry, user_id: str = Depends(get_current_user)):
    db = get_database()
    data = entry.model_dump(exclude=["id"])
    data["user_id"] = user_id
    result = await db.journals.insert_one(data)
    return {"id": str(result.inserted_id), "message": "Journal created successfully"}

@router.get("/")
async def get_journals(user_id: str = Depends(get_current_user)):
    db = get_database()
    cursor = db.journals.find({"user_id": user_id})
    entries = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        entries.append(doc)
    return entries

@router.put("/{entry_id}")
async def update_journal(entry_id: str, entry: JournalEntry, user_id: str = Depends(get_current_user)):
    db = get_database()
    update_data = {k: v for k, v in entry.model_dump(exclude=["id"]).items() if v is not None}
    result = await db.journals.update_one({"_id": ObjectId(entry_id), "user_id": user_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    return {"message": "Updated successfully"}

@router.delete("/{entry_id}")
async def delete_journal(entry_id: str, user_id: str = Depends(get_current_user)):
    db = get_database()
    result = await db.journals.delete_one({"_id": ObjectId(entry_id), "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    return {"message": "Deleted successfully"}

@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...), user_id: str = Depends(get_current_user)):
    file_path = os.path.join(UPLOAD_DIR, f"{user_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"image_url": f"/static/{os.path.basename(file_path)}"}
