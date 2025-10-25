from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import httpx

from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.schemas.token import Token
from app.config import settings

router = APIRouter()

# Endpoint để đăng nhập và nhận token
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):    
    # Gọi API Keycloak để lấy token
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token",
                data={
                    "grant_type": "password",
                    "client_id": settings.KEYCLOAK_CLIENT_ID,
                    "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
                    "username": form_data.username,
                    "password": form_data.password,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            response.raise_for_status()
            tokens = response.json()

            return {
                "access_token": tokens["access_token"],
                "refresh_token": tokens.get("refresh_token", ""),
                "token_type": tokens["token_type"],
            }
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Keycloak authentication failed: {e.response.text}",
            )


@router.post("/token/refresh", response_model=Token)
async def refresh_access_token(refresh_token: str):
    # Gọi API Keycloak để làm mới token
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token",
                data={
                    "grant_type": "refresh_token",
                    "client_id": settings.KEYCLOAK_CLIENT_ID,
                    "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
                    "refresh_token": refresh_token,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            response.raise_for_status()
            tokens = response.json()

            return {
                "access_token": tokens["access_token"],
                "refresh_token": tokens.get("refresh_token", ""),
                "token_type": tokens["token_type"],
            }
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Keycloak token refresh failed: {e.response.text}",
            )


# Endpoint để lấy thông tin người dùng hiện tại
@router.post("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


# Endpoint để đăng xuất (logout)
@router.post("/logout")
async def logout_user(refresh_token: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/logout",
                data={
                    "client_id": settings.KEYCLOAK_CLIENT_ID,
                    "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
                    "refresh_token": refresh_token,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            response.raise_for_status()
            return {"detail": "Successfully logged out"}
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Keycloak logout failed: {e.response.text}",
            )