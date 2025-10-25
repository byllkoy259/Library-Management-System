from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import dependencies, schemas
from app.auth import auth_service
from app.models.user import User
from app.dependencies import get_db

router = APIRouter()

# Register user
@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return auth_service.register_user(user, db)


# Login user
@router.post("/login", response_model=schemas.Token)
async def login_user(email: str, password: str, db: Session = Depends(get_db)):
    return await auth_service.login_user(email, password, db)


# Update user details
@router.put("/update", response_model=schemas.UserResponse)
def update_user(user_update: schemas.UserUpdate, db: Session = Depends(get_db),
                current_user: User = Depends(dependencies.get_current_user)):
    return auth_service.update_user(user_update, db, current_user)