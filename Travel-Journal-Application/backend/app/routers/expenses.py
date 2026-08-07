from fastapi import APIRouter, HTTPException
from app.models import Expense
from app.database import get_database, IN_MEMORY_EXPENSES, IN_MEMORY_ARCHIVES
from bson import ObjectId
from datetime import datetime
import uuid

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/")
async def add_expense(expense: Expense):
    data = expense.model_dump(exclude=["id"])
    data["user_id"] = "public_user"
    exp_id = str(uuid.uuid4())
    
    try:
        db = get_database()
        data["_id"] = exp_id
        await db.expenses.insert_one(data)
    except Exception:
        pass

    IN_MEMORY_EXPENSES.append({"_id": exp_id, **data})
    return {"id": exp_id, "message": "Expense added"}

@router.get("/")
async def list_expenses():
    try:
        db = get_database()
        cursor = db.expenses.find()
        expenses = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            expenses.append(doc)
        if expenses:
            return expenses
    except Exception:
        pass
    return IN_MEMORY_EXPENSES

@router.get("/archives")
async def list_archives():
    try:
        db = get_database()
        cursor = db.trip_archives.find().sort("created_at", -1)
        archives = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            archives.append(doc)
        if archives:
            return archives
    except Exception:
        pass
    return IN_MEMORY_ARCHIVES

@router.delete("/archives/{archive_id}")
async def delete_archive(archive_id: str):
    global IN_MEMORY_ARCHIVES
    try:
        db = get_database()
        await db.trip_archives.delete_one({"_id": ObjectId(archive_id)})
    except Exception:
        pass

    IN_MEMORY_ARCHIVES = [a for a in IN_MEMORY_ARCHIVES if a.get("_id") != archive_id]
    return {"message": "Trip history deleted successfully"}

@router.post("/reset")
async def reset_and_archive_expenses():
    global IN_MEMORY_EXPENSES, IN_MEMORY_ARCHIVES
    expenses = list(IN_MEMORY_EXPENSES)
    
    try:
        db = get_database()
        cursor = db.expenses.find()
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            if doc not in expenses:
                expenses.append(doc)
    except Exception:
        pass
    
    if not expenses:
        raise HTTPException(status_code=400, detail="No active expenses to reset")
    
    total_amount = sum(e["amount"] for e in expenses)
    trip_number = len(IN_MEMORY_ARCHIVES) + 1
    archive_id = str(uuid.uuid4())
    
    archive_doc = {
        "_id": archive_id,
        "user_id": "public_user",
        "trip_name": f"Trip #{trip_number}",
        "total_amount": total_amount,
        "expenses": expenses,
        "created_at": datetime.utcnow().isoformat()
    }
    
    try:
        db = get_database()
        await db.trip_archives.insert_one(dict(archive_doc))
        await db.expenses.delete_many({})
    except Exception:
        pass

    IN_MEMORY_ARCHIVES.insert(0, archive_doc)
    IN_MEMORY_EXPENSES.clear()
    
    return {"message": f"Saved as Trip #{trip_number} and cleared current expenses", "trip_name": f"Trip #{trip_number}"}
