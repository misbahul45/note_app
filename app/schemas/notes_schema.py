from pydantic import BaseModel, Field, UUID4
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=50)
    content: Optional[str] = None
    avatar_url: Optional[str] = None

class NoteCreate(NoteBase):
    user_id: UUID4
    tag_ids: Optional[List[UUID4]] = None

class NoteUpdate(NoteBase):
    title: str = Field(..., min_length=1, max_length=255)
    user_id: Optional[UUID4] = None
    tag_ids: Optional[List[UUID4]] = None

class NoteResponse(NoteBase):
    id: UUID
    user_id: Optional[UUID]
    tags: Optional[List[UUID]] = None
    created_datetime: datetime
    updated_datetime: datetime

    class Config:
        orm_mode = True
        from_attributes = True