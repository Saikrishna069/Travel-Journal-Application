from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class JournalEntry(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str
    destination: str
    content: str
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[str] = None

class Expense(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    category: str
    amount: float
    currency: str = "USD"
    description: str
    date: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[str] = None

class ChatMessage(BaseModel):
    message: str
