from fastapi import APIRouter, Depends, HTTPException
from app.models import Expense
from app.database import get_database, IN_MEMORY_EXPENSES, IN_MEMORY_ARCHIVES
from app.utils import get_current_user
from bson import ObjectId
from datetime import datetime
import uuid

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/")
async def add_expense(expense: Expense, user_id: str = Depends(get_current_user)):
    data = expense.model_dump(exclude=["id"])
    data["user_id"] = user_id
    exp_id = str(uuid.uuid4())
    data["_id"] = exp_id
    
    try:
        db = get_database()
        await db.expenses.insert_one(dict(data))
    except Exception:
        pass

    IN_MEMORY_EXPENSES.append(data)
    return {"id": exp_id, "message": "Expense added successfully"}

@router.get("/")
async def list_expenses(user_id: str = Depends(get_current_user)):
    try:
        db = get_database()
        cursor = db.expenses.find({"user_id": user_id}).sort("date", 1)
        expenses = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            expenses.append(doc)
        if expenses:
            return expenses
    except Exception:
        pass
    
    return [e for e in IN_MEMORY_EXPENSES if e.get("user_id") == user_id]

@router.get("/archives")
async def list_archives(user_id: str = Depends(get_current_user)):
    try:
        db = get_database()
        cursor = db.trip_archives.find({"user_id": user_id}).sort("created_at", -1)
        archives = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            archives.append(doc)
        if archives:
            return archives
    except Exception:
        pass

    return [a for a in IN_MEMORY_ARCHIVES if a.get("user_id") == user_id]

@router.delete("/archives/{archive_id}")
async def delete_archive(archive_id: str, user_id: str = Depends(get_current_user)):
    global IN_MEMORY_ARCHIVES
    try:
        db = get_database()
        await db.trip_archives.delete_one({"_id": ObjectId(archive_id), "user_id": user_id})
    except Exception:
        pass

    IN_MEMORY_ARCHIVES = [a for a in IN_MEMORY_ARCHIVES if not (a.get("_id") == archive_id and a.get("user_id") == user_id)]
    return {"message": "Trip history deleted successfully"}

@router.post("/reset")
async def reset_and_archive_expenses(user_id: str = Depends(get_current_user)):
    global IN_MEMORY_EXPENSES, IN_MEMORY_ARCHIVES
    expenses = [e for e in IN_MEMORY_EXPENSES if e.get("user_id") == user_id]
    
    try:
        db = get_database()
        cursor = db.expenses.find({"user_id": user_id})
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            if doc not in expenses:
                expenses.append(doc)
    except Exception:
        pass
    
    if not expenses:
        raise HTTPException(status_code=400, detail="No active expenses to reset")
    
    total_amount = sum(e["amount"] for e in expenses)
    user_archives = [a for a in IN_MEMORY_ARCHIVES if a.get("user_id") == user_id]
    trip_number = len(user_archives) + 1
    archive_id = str(uuid.uuid4())
    
    archive_doc = {
        "_id": archive_id,
        "user_id": user_id,
        "trip_name": f"Trip #{trip_number}",
        "total_amount": total_amount,
        "expenses": expenses,
        "created_at": datetime.utcnow().isoformat()
    }
    
    try:
        db = get_database()
        await db.trip_archives.insert_one(dict(archive_doc))
        await db.expenses.delete_many({"user_id": user_id})
    except Exception:
        pass

    IN_MEMORY_ARCHIVES.insert(0, archive_doc)
    IN_MEMORY_EXPENSES = [e for e in IN_MEMORY_EXPENSES if e.get("user_id") != user_id]
    
    return {"message": f"Saved as Trip #{trip_number} and cleared current expenses", "trip_name": f"Trip #{trip_number}"}
