from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import dependencies, models
from app.models.user import User
from app.schemas.category import CategoryResponse


router = APIRouter()

add_pagination(router)

@router.get("/", response_model=Page[CategoryResponse])
def get_categories(name: str = Query(None, description="Search categories by name"),
                   db: Session = Depends(dependencies.get_db),
                   current_user: User = Depends(dependencies.require_user),
                   order_by: Literal["id", "name"] = Query("id"),
                   sort: Literal["asc", "desc"] = Query("asc")):
    column = {
        "id": models.Category.id,
        "name": models.Category.name
    }

    order_column = column.get(order_by, models.Category.id)

    if sort == "desc":
        order_column = order_column.desc()
    elif sort == "asc":
        order_column = order_column.asc()
    
    categories = db.query(models.Category).order_by(order_column).all()

    if not categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No categories found"
        )

    query = db.query(
        models.Category.id,
        models.Category.name,
        models.Category.description,
        models.Category.created_at,
        models.Category.updated_at,
        func.count(models.Book.id).label("book_count")
    ).outerjoin(models.Book, models.Book.category_id == models.Category.id)\
    .group_by(models.Category.id)\
    .order_by(order_column)

    if name:
        query = query.filter(models.Category.name.ilike(f"%{name}%"))

    results = query.all()
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No matching categories found"
        )

    return paginate(results)