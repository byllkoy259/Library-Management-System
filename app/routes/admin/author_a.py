from datetime import datetime, timezone
from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy.orm import Session

from app import dependencies, models
from app.dependencies import get_db
from app.models.author import Author
from app.models.user import User
from app.schemas.author import AuthorCreate, AuthorResponse, AuthorUpdate


router = APIRouter()

add_pagination(router)

# Get all authors
@router.get("/", response_model=Page[AuthorResponse])
def get_authors(name: str = Query(None, description="Search by author's name"),
                db: Session = Depends(get_db),
                current_user: User = Depends(dependencies.require_admin),
                order_by: Literal["id", "name"] = Query("id"),
                sort: Literal["asc", "desc"] = Query("asc")):
    column = {
        "id": models.Author.id,
        "name": models.Author.name
    }

    order_column = column.get(order_by, models.Author.id)
    if sort == "desc":
        order_column = order_column.desc()
    elif sort == "asc":
        order_column = order_column.asc()

    authors = db.query(models.Author).order_by(order_column).all()

    if not authors:
        raise HTTPException(status_code=404, detail="No authors found")
    return paginate(authors)


# Create a new author
@router.post("/add", response_model=AuthorResponse)
def add_author(author: AuthorCreate, db: Session = Depends(get_db),
               current_user: User = Depends(dependencies.require_admin)):
    new_author = Author(
        name=author.name,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    author_response = AuthorResponse(
        id=new_author.id,
        name=new_author.name,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    return author_response

# Update author info
@router.put("/update/{author_id}", response_model=AuthorResponse)
def update_author(author_id: int, author: AuthorUpdate, db: Session = Depends(get_db),
               current_user: User = Depends(dependencies.require_admin)):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    for key, value in author.dict(exclude_unset=True).items():
        setattr(db_author, key, value)
    db_author.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_author)

    author_response = AuthorResponse(
        id=db_author.id,
        name=db_author.name,
        created_at=db_author.created_at,
        updated_at=db_author.updated_at
    )
    return author_response

# Delete author info
@router.delete("/delete/{author_id}", status_code=200)
def delete_author(author_id: int, db: Session = Depends(get_db),
               current_user: User = Depends(dependencies.require_admin)):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    db.delete(db_author)
    db.commit()
    print(f"Author with ID {author_id} deleted successfully.")
    return {"detail": "Author deleted successfully"}