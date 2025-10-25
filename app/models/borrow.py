from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.database import Base

class BorrowStatus(enum.Enum):
    borrowing = "borrowing"
    returned = "returned"
    overdue = "overdue"

class Borrow(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    borrow_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True) # Sẽ null cho đến khi sách được trả
    
    status = Column(Enum(BorrowStatus), default=BorrowStatus.borrowing, nullable=False)

    # SQLAlchemy relationships
    book = relationship("Book")
    user = relationship("User")