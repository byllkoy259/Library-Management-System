from datetime import datetime, timezone
from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app import dependencies, models
from app.models.book import Book
from app.models.user import User
from app.routes.admin.user_manage_a import get_db
from app.schemas.book import BookCreate, BookResponse, BookUpdate

router = APIRouter()

add_pagination(router)

# Get all books
@router.get("/", response_model=Page[BookResponse])
def get_books(title: str = Query(None, description="Search books by title"),
              author: str = Query(None, description="Search books by author"),
              category: str = Query(None, description="Search books by category"),
              db: Session = Depends(get_db), 
              current_user: User = Depends(dependencies.require_admin),
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


# Create a new book
@router.post("/add", response_model=BookResponse)
def add_book(book: BookCreate, db: Session = Depends(get_db), 
             current_user: User = Depends(dependencies.require_admin)):
    category = db.query(models.Category).filter(models.Category.id == book.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    new_book = Book(
        title=book.title, 
        main_author_id=book.main_author_id, 
        description=book.description,
        quantity=book.quantity,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        category_id=book.category_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    # Thêm các tác giả phụ nếu có
    if book.book_authors:
        for author_id in book.book_authors:
            book_author = models.BookAuthor(book_id=new_book.id, author_id=author_id)
            db.add(book_author)
        db.commit()

    book_response = BookResponse(
        id=new_book.id,
        title=new_book.title,
        main_author=new_book.main_author,
        authors=[ba.author for ba in new_book.book_authors],
        description=new_book.description,
        quantity=new_book.quantity,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        category_id=new_book.category_id,
        category=new_book.category.name if new_book.category else None
    )
    return book_response


# Update book details
@router.put("/update/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_data: BookUpdate, db: Session = Depends(get_db), 
                current_user: User = Depends(dependencies.require_admin)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Kiểm tra nếu category_id được thay đổi
    if book_data.category_id is not None:
        category = db.query(models.Category).filter(models.Category.id == book_data.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    else:
        category = book.category  # Giữ lại category hiện tại để trả response

    for key, value in book_data.dict(exclude_unset=True).items():
        if key != "book_authors":
            setattr(book, key, value)
    book.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(book)

    # Cập nhật các tác giả phụ nếu có
    if book_data.book_authors is not None:
        # Xoá các tác giả phụ hiện tại
        db.query(models.BookAuthor).filter(models.BookAuthor.book_id == book.id).delete()
        db.commit()

        # Thêm các tác giả phụ mới
        for author_id in book_data.book_authors:
            book_author = models.BookAuthor(book_id=book.id, author_id=author_id)
            db.add(book_author)
        db.commit()

    book_response = BookResponse(
        id=book.id,
        title=book.title,
        main_author=book.main_author,
        authors=[ba.author for ba in book.book_authors],
        description=book.description,
        quantity=book.quantity,
        created_at=book.created_at,
        updated_at=book.updated_at,
        category_id=book.category_id,
        category=book.category.name if book.category else None
    )
    return book_response


# Delete a book
@router.delete("/delete/{book_id}", status_code=200)
def delete_book(book_id: int, db: Session = Depends(get_db), 
                current_user:  User = Depends(dependencies.require_admin)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    print(f"Book with ID {book_id} deleted successfully.")
    return {"detail": "Book deleted successfully"}