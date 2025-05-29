from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.middleware import auth_dependency
from app.core.security import hash_password
from app.db import get_db
from app.db.models import User as DBUser  # SQLAlchemy model
from app.schemas import APIResponse
from app.schemas.users_schema import UserCreate, UserUpdate, UserResponse
from uuid import UUID

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@users_router.get(
    "/",
    response_model=APIResponse[List[UserResponse]]
)
async def get_users(db: Session = Depends(get_db)) -> APIResponse[List[UserResponse]]:
    users = db.query(DBUser).all()
    user_responses = [UserResponse.model_validate(user) for user in users]
    return APIResponse[List[UserResponse]](
        status="success",
        message="Successfully get users",
        data={"users": user_responses}  # Pass a dictionary with "users" key
    )

@users_router.get(
    "/{user_id}",
    response_model=APIResponse[UserResponse]
)
async def get_user(user_id: UUID, db: Session = Depends(get_db)) -> APIResponse[UserResponse] | Any:
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user:
        return {"message": f"User {user_id} not found"}
    return APIResponse[UserResponse](
        status="success",
        message=f"Successfully get user {user_id}",
        data={"user": user}  # Pass a dictionary with "user" key
    )

@users_router.post(
    "/",
    dependencies=[Depends(auth_dependency)],
    response_model=APIResponse[None]
)
async def create_user(new_user: UserCreate, db: Session = Depends(get_db)) -> APIResponse[None]:
    db_user = DBUser(
        username=new_user.username,
        email=new_user.email,
        password=hash_password(new_user.password),
        avatar_url=new_user.avatar_url
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return APIResponse[None](
        status="success",
        message="Successfully created user",
        data=None
    )

@users_router.patch(
    "/{user_id}",
    dependencies=[Depends(auth_dependency)],
    response_model=APIResponse[None]
)
async def update_user(user_id: UUID, user_update: UserUpdate, db: Session = Depends(get_db)) -> APIResponse[None] | Any:
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user:
        return {"message": f"User {user_id} not found"}
    if user_update.username:
        setattr(user, 'username', user_update.username)
    if user_update.email:
        setattr(user, 'email', user_update.email)
    if user_update.password:
        setattr(user, 'password', hash_password(user_update.password))
    if user_update.avatar_url:
        setattr(user, 'avatar_url', user_update.avatar_url)
    db.commit()
    db.refresh(user)
    return APIResponse[None](
        status="success",
        message=f"Successfully updated user {user.username}",
        data=None
    )

@users_router.delete(
    "/{user_id}",
    dependencies=[Depends(auth_dependency)],
    response_model=APIResponse[None]
)
async def delete_user(user_id: UUID, db: Session = Depends(get_db)) -> APIResponse[None] | Any:
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user:
        return {"message": f"User {user_id} not found"}
    db.delete(user)
    db.commit()
    return APIResponse[None](
        status="success",
        message=f"Successfully deleted user {user_id}",
        data=None
    )