from typing import Generic, TypeVar, Dict, Optional
from pydantic import BaseModel
from .auth_schema import *

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    status: str
    message: str
    data: Optional[Dict[str, T]] = None

    def __init__(self, status: str, message: str, data: Optional[Dict[str, T]] = None):
        super().__init__(
            status=status,
            message=message,
            data=data if data else None
        )

    class Config:
        from_attributes = True