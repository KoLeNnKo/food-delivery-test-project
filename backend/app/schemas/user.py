from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    address: Optional[str] = None

class UserChangePassword(BaseModel):
    old_password: str
    new_password: str

class UserInDB(UserBase):
    id: int
    role: str
    address: Optional[str] = None

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"