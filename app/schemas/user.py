from datetime import date, datetime, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.schemas.role import RoleResponse

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    dob: Optional[date] = None
    role_id: Optional[int] = 2

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    dob: Optional[date] = None

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone: Optional[str] = None
    dob: Optional[date] = None
    is_active: int
    role: RoleResponse
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True