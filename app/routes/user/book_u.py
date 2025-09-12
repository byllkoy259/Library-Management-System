from datetime import datetime, timezone
from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app import dependencies, models
from app.dependencies import get_db
from app.models.user import User
from app.schemas.book import BookResponse

router = APIRouter()

add_pagination(router)

# Get all books
@router.get("/", response_model=Page[BookResponse])
def get_books(title: str = Query(None, description="Search books by title"),
              author: str = Query(None, description="Search books by author"),
              category: str = Query(None, description="Search books by category"),
              db: Session = Depends(get_db), 
              current_user: User = Depends(dependencies.require_user),
              order_by: Literal["id", "title"] = Query("id"),
              sort: Literal["asc", "desc"] = Query("asc")):
    column = {
        "id": models.Book.id,
        "title": models.Book.title
    }

    order_column = column.get(order_by, models.Book.id)

    if sort == "desc":
        order_column = order_column.desc()
    elif sort == "asc":
        order_column = order_column.asc()

    query = db.query(models.Book)\
            .options(joinedload(models.Book.main_author),
                     joinedload(models.Book.book_authors).joinedload(models.BookAuthor.author),
                     joinedload(models.Book.category)
                     )\
            .group_by(models.Book.id)\
            .order_by(order_column)
    
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if author:
        subquery = db.query(models.BookAuthor.book_id)\
                    .join(models.Author)\
                    .filter(models.Author.name.ilike(f"%{author}%"))\
                    .subquery()
        query = query.outerjoin(models.Book.main_author)\
                    .filter(
                        or_(
                            models.Author.name.ilike(f"%{author}%"),
                            models.Book.id.in_(subquery)
                        )
                    )
    if category:
        query = query.filter(models.Book.category.has(models.Category.name.ilike(f"%{category}%")))
    
    books = query.all()
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    
    book_response = []
    for book in books:
        book_response.append(BookResponse(
            id=book.id,
            title=book.title,
            main_author=book.main_author,
            authors=[ba.author for ba in book.book_authors],
            description=book.description,
            quantity=book.quantity,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            category_id=book.category_id,
            category=book.category.name if book.category else None
        ))
    return paginate(book_response)