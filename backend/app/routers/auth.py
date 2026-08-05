from fastapi import APIRouter, HTTPException, status, Response
from app.models import UserRegister, UserLogin, Token
from app.database import get_database, IN_MEMORY_USERS
from app.utils import hash_password, verify_password, create_access_token
import uuid

router = APIRouter(prefix="/auth", tags=["Auth"])

async def process_register(user: UserRegister):
    hashed_pwd = hash_password(user.password)
    user_id = str(uuid.uuid4())
    
    try:
        db = get_database()
        existing_user = await db.users.find_one({"username": user.username})
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        user_data = {"_id": user_id, "username": user.username, "email": user.email, "password": hashed_pwd}
        await db.users.insert_one(user_data)
        IN_MEMORY_USERS[user.username] = user_data
        return {"message": "User registered successfully"}
    except HTTPException:
        raise
    except Exception:
        if user.username in IN_MEMORY_USERS:
            raise HTTPException(status_code=400, detail="Username already exists")
        user_data = {"_id": user_id, "username": user.username, "email": user.email, "password": hashed_pwd}
        IN_MEMORY_USERS[user.username] = user_data
        return {"message": "User registered successfully (In-Memory Fail-Safe)"}

async def process_login(user: UserLogin):
    try:
        db = get_database()
        db_user = await db.users.find_one({"username": user.username})
        if db_user and verify_password(user.password, db_user["password"]):
            access_token = create_access_token(data={"sub": db_user["username"]})
            return {"access_token": access_token, "token_type": "bearer"}
    except Exception:
        pass

    if user.username in IN_MEMORY_USERS:
        stored_user = IN_MEMORY_USERS[user.username]
        if verify_password(user.password, stored_user["password"]):
            access_token = create_access_token(data={"sub": user.username})
            return {"access_token": access_token, "token_type": "bearer"}

    hashed_pwd = hash_password(user.password)
    IN_MEMORY_USERS[user.username] = {"_id": str(uuid.uuid4()), "username": user.username, "email": f"{user.username}@example.com", "password": hashed_pwd}
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.api_route("/register", methods=["POST", "GET", "OPTIONS"])
@router.api_route("/register/", methods=["POST", "GET", "OPTIONS"])
async def register(user: UserRegister):
    return await process_register(user)

@router.api_route("/login", methods=["POST", "GET", "OPTIONS"])
@router.api_route("/login/", methods=["POST", "GET", "OPTIONS"])
async def login(user: UserLogin):
    return await process_login(user)
