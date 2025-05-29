from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db.models import User
from app.services.auth_services import decode_acces_token
def hash_password(password: str) -> str:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)


def get_current_user(token:str, db:Session) -> User:
    payload=decode_acces_token(token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )
    user_id=payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )
    user=db.query(User).get(user_id)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )
    return user