from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)

    main_author_id = Column(Integer, ForeignKey("authors.id"))
    main_author = relationship("Author", back_populates="main_author", foreign_keys=[main_author_id])

    description = Column(String(500), nullable=True)
    quantity = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="books")

    book_authors = relationship("BookAuthor", back_populates="book", cascade="all, delete")