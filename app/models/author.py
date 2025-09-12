from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    main_author = relationship("Book", back_populates="main_author", foreign_keys="Book.main_author_id")
    book_authors = relationship("BookAuthor", back_populates="author", cascade="all, delete")