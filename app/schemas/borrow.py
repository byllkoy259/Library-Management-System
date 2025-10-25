from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from .book import BookResponse 

class BorrowBase(BaseModel):
    book_id: int

class BorrowCreate(BorrowBase):
    pass

class BorrowResponse(BaseModel):
    id: int
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    status: str
    book: BookResponse

    class Config:
        from_attributes = True # Đổi từ orm_mode trong Pydantic v2