from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Union
from jose import jwt
from app.core.settings import get_settings


def create_access_token(
    data: Dict[str, Any], 
    expires_delta: Union[timedelta, None] = None
) -> str:
    to_encode = data.copy()

    for key, value in to_encode.items():
        if hasattr(value, 'hex'): 
            to_encode[key] = str(value)

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, 
        get_settings().JWT_SECRET_KEY, 
        algorithm=get_settings().JWT_ALGORITHM
    )
    return encoded_jwt
