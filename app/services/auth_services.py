from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.settings import get_settings
from typing import Any

def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode=data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=get_settings().JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt=jwt.encode(to_encode, get_settings().JWT_SECRET_KEY, algorithm=get_settings().JWT_ALGORITHM)
    return encoded_jwt