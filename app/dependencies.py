from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.auth.jwt_handler import verify_token, get_user_info
from app.config import settings
from datetime import datetime, timezone

# Cấu hình OAuth2 với Keycloak
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = await verify_token(token)
    print("User info:", payload)

    if payload is None or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Lấy thông tin user từ token
    user_info = get_user_info(payload)
    keycloak_username = user_info.get("username")
    
    if not keycloak_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username not found"
        )
    
    # Tìm user trong local DB
    user = db.query(User).filter(User.username == keycloak_username).first()
    
    if user is None:
        # JIT User Provisioning - tạo user mới nếu chưa có
        user = create_user_from_keycloak(db, user_info)
    
    user.keycloak_roles = user_info.get("roles", [])
    user.keycloak_info = user_info
    
    return user

def create_user_from_keycloak(db: Session, user_info: dict) -> User:
    """JIT User Provisioning"""
    
    # Tạo user mới từ thông tin Keycloak
    new_user = User(
        username=user_info.get("username"),
        email=user_info.get("email"),
        hashed_password="", # Không cần password vì auth qua Keycloak
        phone=None, # Có thể map từ custom claims
        dob=None,
        is_active=1,
        role_id=1, # Default role, có thể map từ Keycloak roles
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


async def require_admin(current_user: User = Depends(get_current_user)):
    # Kiểm tra role từ Keycloak
    if hasattr(current_user, 'keycloak_roles') and "admin" in current_user.keycloak_roles:
        return current_user
    
    # Fallback: kiểm tra role từ local DB
    if current_user.role and current_user.role.name == "admin":
        return current_user
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Admin privileges required"
    )


async def require_user(current_user: User = Depends(get_current_user)):
    # Kiểm tra role từ Keycloak
    if hasattr(current_user, 'keycloak_roles') and "user" in current_user.keycloak_roles:
        return current_user
    
    # Fallback: kiểm tra role từ local DB
    if current_user.role and current_user.role.name == "user":
        return current_user
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User privileges required"
    )