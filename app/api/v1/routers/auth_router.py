from datetime import timedelta
from typing import Any 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password
from app.core.settings import get_settings
from app.db import get_db
from app.db.models import User
from app.schemas import APIResponse
from app.schemas.users_schema import Login, Register
from app.services.auth_services import create_access_token

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}}
)

otp_setorage={}

@auth_router.post("/login", response_model=APIResponse[Any])
async def login(user_login:Login, db:Session=Depends(get_db)) -> APIResponse[Any]:
    db_user = db.query(User).filter(User.email == user_login.email).first()
    if not db_user:
        raise HTTPException(
            status_code=404, 
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    isMatch = verify_password(user_login.password, getattr(db_user, 'password'))

    if not isMatch:
        raise HTTPException(
            status_code=401, 
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires=timedelta(minutes=get_settings().JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token :str =create_access_token(
        data={"sub":str(db_user.id), "email": db_user.email},
        expires_delta=access_token_expires
    )

    return APIResponse(
        message="Successfully login",
        status="success",
        data={
            "access_token": access_token,
        }
    )

@auth_router.post("/register", response_model=APIResponse[None])
async def register(user_register:Register, db:Session=Depends(get_db)) -> APIResponse[None]:
    db_user=db.query(User).filter(User.username == user_register.username or User.email == user_register.email).first()
    if db_user:
        raise HTTPException(
            status_code=400, 
            detail="Username or email already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    hashed_password=hash_password(user_register.password)
    new_user = User(
        username=user_register.username,
        email=user_register.email,
        password=hashed_password,
        avatar_url=user_register.avatar_url
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return APIResponse(
        status="success",
        message="User registered successfully",
        data=None
    )
