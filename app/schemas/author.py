from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class AuthorCreate(BaseModel):
    name: str

class AuthorUpdate(BaseModel):
    name: Optional[str] = None

class AuthorResponse(BaseModel):
    id: int
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True