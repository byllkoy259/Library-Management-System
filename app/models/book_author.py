from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class BookAuthor(Base):
    __tablename__ = "book_authors"
    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), primary_key=True, nullable=False)

    book = relationship("Book", back_populates="book_authors")
    author = relationship("Author", back_populates="book_authors")