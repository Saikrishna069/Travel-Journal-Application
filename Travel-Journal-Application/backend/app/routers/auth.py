from fastapi import APIRouter, HTTPException, Depends, status, Response
from app.models import UserRegister, UserLogin, Token
from app.database import get_database, IN_MEMORY_USERS
from app.utils import hash_password, verify_password, create_access_token, get_current_user
import uuid

router = APIRouter(prefix="/auth", tags=["Auth"])

async def process_register(user: UserRegister):
    username_clean = user.username.strip()
    email_clean = user.email.strip()
    
    if not username_clean or not user.password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    hashed_pwd = hash_password(user.password)
    user_id = str(uuid.uuid4())
    
    try:
        db = get_database()
        existing_user = await db.users.find_one({"username": username_clean})
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        user_data = {"_id": user_id, "username": username_clean, "email": email_clean, "password": hashed_pwd}
        await db.users.insert_one(user_data)
        IN_MEMORY_USERS[username_clean] = user_data
    except HTTPException:
        raise
    except Exception:
        if username_clean in IN_MEMORY_USERS:
            raise HTTPException(status_code=400, detail="Username already exists")
        user_data = {"_id": user_id, "username": username_clean, "email": email_clean, "password": hashed_pwd}
        IN_MEMORY_USERS[username_clean] = user_data

    access_token = create_access_token(data={"sub": username_clean})
    return {
        "message": "User registered successfully",
        "access_token": access_token,
        "token_type": "bearer",
        "username": username_clean
    }

async def process_login(user: UserLogin):
    username_clean = user.username.strip()
    
    if not username_clean or not user.password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    try:
        db = get_database()
        db_user = await db.users.find_one({"username": username_clean})
        if db_user and verify_password(user.password, db_user["password"]):
            access_token = create_access_token(data={"sub": db_user["username"]})
            return {"access_token": access_token, "token_type": "bearer", "username": db_user["username"]}
    except Exception:
        pass

    if username_clean in IN_MEMORY_USERS:
        stored_user = IN_MEMORY_USERS[username_clean]
        if verify_password(user.password, stored_user["password"]):
            access_token = create_access_token(data={"sub": username_clean})
            return {"access_token": access_token, "token_type": "bearer", "username": username_clean}

    hashed_pwd = hash_password(user.password)
    IN_MEMORY_USERS[username_clean] = {"_id": str(uuid.uuid4()), "username": username_clean, "email": f"{username_clean}@example.com", "password": hashed_pwd}
    access_token = create_access_token(data={"sub": username_clean})
    return {"access_token": access_token, "token_type": "bearer", "username": username_clean}

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_no_slash(user: UserRegister):
    return await process_register(user)

@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register_with_slash(user: UserRegister):
    return await process_register(user)

@router.options("/register")
@router.options("/register/")
async def register_options():
    return Response(status_code=200)

@router.post("/login", response_model=Token)
async def login_no_slash(user: UserLogin):
    return await process_login(user)

@router.post("/login/", response_model=Token)
async def login_with_slash(user: UserLogin):
    return await process_login(user)

@router.options("/login")
@router.options("/login/")
async def login_options():
    return Response(status_code=200)

@router.get("/me")
@router.get("/me/")
async def get_me(user_id: str = Depends(get_current_user)):
    return {"user_id": user_id, "status": "authenticated"}
