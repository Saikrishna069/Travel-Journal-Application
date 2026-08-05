from fastapi import APIRouter, HTTPException, Depends, status
from app.models import UserRegister, UserLogin, Token
from app.database import get_database
from app.utils import hash_password, verify_password, create_access_token
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister):
    try:
        db = get_database()
        existing_user = await db.users.find_one({"username": user.username})
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        hashed_pwd = hash_password(user.password)
        user_data = {"username": user.username, "email": user.email, "password": hashed_pwd}
        await db.users.insert_one(user_data)
        return {"message": "User registered successfully"}
    except (ServerSelectionTimeoutError, PyMongoError) as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed. Please ensure MongoDB service is running or set MONGO_URI in backend/.env"
        )

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    try:
        db = get_database()
        db_user = await db.users.find_one({"username": user.username})
        if not db_user or not verify_password(user.password, db_user["password"]):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        access_token = create_access_token(data={"sub": db_user["username"]})
        return {"access_token": access_token, "token_type": "bearer"}
    except (ServerSelectionTimeoutError, PyMongoError) as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed. Please ensure MongoDB service is running or set MONGO_URI in backend/.env"
        )
