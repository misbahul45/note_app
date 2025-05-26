from datetime import datetime
from uuid import UUID as PyUUID
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Untuk NoteSummary jika diperlukan di skema User
class NoteSummary(BaseModel):
    id: PyUUID
    title: str
    created_datetime: datetime

    class Config:
        from_attributes = True