from fastapi import APIRouter, Depends, HTTPException
from app.models import Expense
from app.database import get_database
from app.utils import get_current_user
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/")
async def add_expense(expense: Expense, user_id: str = Depends(get_current_user)):
    db = get_database()
    data = expense.model_dump(exclude=["id"])
    data["user_id"] = user_id
    result = await db.expenses.insert_one(data)
    return {"id": str(result.inserted_id), "message": "Expense added"}

@router.get("/")
async def list_expenses(user_id: str = Depends(get_current_user)):
    db = get_database()
    cursor = db.expenses.find({"user_id": user_id})
    expenses = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        expenses.append(doc)
    return expenses

@router.get("/archives")
async def list_archives(user_id: str = Depends(get_current_user)):
    db = get_database()
    cursor = db.trip_archives.find({"user_id": user_id}).sort("created_at", -1)
    archives = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        archives.append(doc)
    return archives

@router.delete("/archives/{archive_id}")
async def delete_archive(archive_id: str, user_id: str = Depends(get_current_user)):
    db = get_database()
    result = await db.trip_archives.delete_one({"_id": ObjectId(archive_id), "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Saved trip archive not found")
    return {"message": "Trip history deleted successfully"}

@router.post("/reset")
async def reset_and_archive_expenses(user_id: str = Depends(get_current_user)):
    db = get_database()
    cursor = db.expenses.find({"user_id": user_id})
    expenses = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        expenses.append(doc)
    
    if not expenses:
        raise HTTPException(status_code=400, detail="No active expenses to reset")
    
    total_amount = sum(e["amount"] for e in expenses)
    count = await db.trip_archives.count_documents({"user_id": user_id})
    trip_number = count + 1
    
    archive_doc = {
        "user_id": user_id,
        "trip_name": f"Trip #{trip_number}",
        "total_amount": total_amount,
        "expenses": expenses,
        "created_at": datetime.utcnow()
    }
    
    await db.trip_archives.insert_one(archive_doc)
    await db.expenses.delete_many({"user_id": user_id})
    
    return {"message": f"Saved as Trip #{trip_number} and cleared current expenses", "trip_name": f"Trip #{trip_number}"}
