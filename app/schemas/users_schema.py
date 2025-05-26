from pydantic import BaseModel, EmailStr

class Register(BaseModel):
    username: str
    email: EmailStr
    password: str
    avatar_url: str | None = None

class Login(BaseModel):
    email: EmailStr
    password: str