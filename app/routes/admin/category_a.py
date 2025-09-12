from datetime import datetime, timezone
from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import dependencies, models
from app.dependencies import get_db
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate

router = APIRouter()

add_pagination(router)

# Get all categories
@router.get("/", response_model=Page[CategoryResponse])
def get_categories(name: str = Query(None, description="Search categories by name"),
                   db: Session = Depends(get_db),
                   current_user: User = Depends(dependencies.require_admin),
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
        raise HTTPException(status_code=404, detail="No categories found")
    
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

    print(query)
    results = query.all()
    if not results:
        raise HTTPException(status_code=404, detail="No matching categories found")
    return paginate(results)


# Create a new category
@router.post("/add", response_model=CategoryResponse)

def create_category(category: CategoryCreate, db: Session = Depends(get_db),
                    current_user: User = Depends(dependencies.require_admin)):
    new_category = Category(
        name=category.name,
        description=category.description,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    category_response = CategoryResponse(
        id=new_category.id,
        name=new_category.name,
        description=new_category.description,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        book_count=db.query(func.count(models.Book.id)).filter(models.Book.category_id == new_category.id).scalar()
    )
    return category_response


# Update category details
@router.put("/update/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db),
                    current_user: User = Depends(dependencies.require_admin)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)
    db_category.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_category)
    
    category_response = CategoryResponse(
        id=db_category.id,
        name=db_category.name,
        description=db_category.description,
        created_at=db_category.created_at,
        updated_at=db_category.updated_at,
        book_count=db.query(func.count(models.Book.id)).filter(models.Book.category_id == db_category.id).scalar()
    )
    return category_response


# Delete a category
@router.delete("/delete/{category_id}", status_code=200)
def delete_category(category_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(dependencies.require_admin)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(db_category)
    db.commit()
    print(f"Category with ID {category_id} deleted successfully.")
    return {"detail": "Category deleted successfully"}