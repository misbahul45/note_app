from pydantic import BaseModel, EmailStr, Field

class Register(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    avatar_url: str | None = None

class Login(BaseModel):
    email: EmailStr
    password: str