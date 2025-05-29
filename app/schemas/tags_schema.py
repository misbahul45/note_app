from pydantic import BaseModel, UUID4, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)  # Nama tag wajib, unik, dengan batasan panjang

class TagCreate(TagBase):
    pass  

# Schema untuk memperbarui Tag
class TagUpdate(TagBase):
    pass 

# Schema untuk respons Tag (termasuk ID dan timestamps)
class TagResponse(TagBase):
    id: UUID
    created_datetime: datetime
    updated_datetime: datetime
    notes: Optional[List[UUID]] = None 

    class Config:
        orm_mode = True  
        from_attributes = True  

class TagDelete(BaseModel):
    id: UUID4