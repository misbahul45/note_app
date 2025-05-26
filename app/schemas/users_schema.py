from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID as PyUUID
from app.schemas.notes_schema import NoteSummary


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    email: EmailStr
    avatar_url: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=6)
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None

class UserResponse(BaseModel):
    id: PyUUID
    username: str
    email: EmailStr
    avatar_url: Optional[str]
    created_datetime: datetime
    updated_datetime: datetime
    notes: Optional[List[NoteSummary]] = []

    class Config:
        from_attributes = True
