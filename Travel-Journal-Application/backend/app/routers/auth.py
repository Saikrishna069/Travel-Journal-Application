from fastapi import APIRouter, HTTPException, Depends, status, Response
from app.models import Token
from app.utils import create_access_token, get_current_user
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter(prefix="/auth", tags=["Auth"])

class AccessRequest(BaseModel):
    passcode: str
    username: Optional[str] = "Traveler"

@router.post("/access", status_code=status.HTTP_200_OK)
@router.post("/access/", status_code=status.HTTP_200_OK)
@router.post("/login", status_code=status.HTTP_200_OK)
@router.post("/login/", status_code=status.HTTP_200_OK)
async def grant_access(req: AccessRequest):
    user_name = req.username.strip() if req.username else "Traveler"
    access_token = create_access_token(data={"sub": user_name})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user_name,
        "message": "Access Granted"
    }

@router.options("/access")
@router.options("/access/")
@router.options("/login")
@router.options("/login/")
async def options_handler():
    return Response(status_code=200)

@router.get("/me")
@router.get("/me/")
async def get_me(user_id: str = Depends(get_current_user)):
    return {"user_id": user_id, "status": "authenticated"}
