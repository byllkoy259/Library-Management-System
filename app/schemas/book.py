from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from app.schemas.author import AuthorResponse
from app.schemas.category import CategoryResponse

class BookCreate(BaseModel):
    title: str
    main_author_id: int
    description: Optional[str] = None
    quantity: int = 0
    category_id: int
    book_authors: Optional[list[int]] = []

class BookUpdate(BaseModel):
    title: Optional[str] = None
    main_author_id: Optional[int] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    category_id: Optional[int] = None
    book_authors: Optional[list[int]] = None

class BookResponse(BaseModel):
    id: int
    title: str
    main_author: AuthorResponse
    authors: list[AuthorResponse] = []
    description: Optional[str] = None
    quantity: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    category_id: int
    category: Optional[str] = None

    class Config:
        from_attributes = True