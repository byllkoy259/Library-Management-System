from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy.orm import Session

from app import dependencies, models, schemas
from app.models.user import User
from app.dependencies import get_db

router = APIRouter()

add_pagination(router)

# Get all users
@router.get("/", response_model=Page[schemas.UserResponse])
def get_users(db: Session = Depends(get_db),
                  current_user: User = Depends(dependencies.require_admin),
                  order_by: Literal["id", "username", "email"] = Query("id"),
                  sort: Literal["asc", "desc"] = Query("asc")):
    column = {
        "id": models.User.id,
        "username": models.User.username,
        "email": models.User.email
    }

    order_column = column.get(order_by, models.User.id)

    if sort == "desc":
        order_column = order_column.desc()
    elif sort == "asc":
        order_column = order_column.asc()

    users = db.query(models.User).order_by(order_column).all()
    
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return paginate(users)


# Delete user by ID
@router.delete("/{user_id}", status_code=200)
def delete_user(user_id: int, db: Session = Depends(get_db), 
                current_user: User = Depends(dependencies.require_admin)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    print(f"User with ID {user_id} deleted successfully.")
    return {"detail": "User deleted successfully"}