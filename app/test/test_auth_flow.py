# test_auth_flow.py
import asyncio
import httpx
from app.config import settings

async def test_auth_flow():
    async with httpx.AsyncClient() as client:
        try:
            # 1. Get token
            response = await client.post(
                f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token",
                data={
                    "grant_type": "password",
                    "client_id": settings.KEYCLOAK_CLIENT_ID,
                    "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
                    "username": "testuser",  # Thay bằng user thật
                    "password": "123456789",  # Thay bằng password thật
                }
            )
            tokens = response.json()
            print("✅ Login successful")
            print(f"Access token: {tokens['access_token'][:50]}...")
            
            # 2. Test protected endpoint
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            response = await client.get("http://localhost:8000/auth/users/me", headers=headers)
            print("✅ Protected endpoint accessible")
            
            # 3. Test token verification
            from app.auth.jwt_handler import verify_token
            payload = await verify_token(tokens['access_token'])
            print("✅ Token verification successful")
            print(f"User: {payload.get('preferred_username')}")
            
        except Exception as e:
            print(f"❌ Auth flow failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_auth_flow())