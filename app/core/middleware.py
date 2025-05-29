from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db import get_db


security = HTTPBearer()

async def auth_dependency(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Dependency function untuk autentikasi
    Bisa digunakan di route manapun yang butuh auth
    """
    if not credentials:
        raise HTTPException(status_code=401, detail="Token required")
    
    token = credentials.credentials
    current_user = get_current_user(token, db)
    return current_user