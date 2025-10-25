import asyncio
import httpx
from app.config import settings

async def test_keycloak_connection():
    try:
        async with httpx.AsyncClient() as client:
            # Test JWKS endpoint
            response = await client.get(
                f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"
            )
            print("✅ JWKS endpoint accessible")
            
            # Test realm info
            response = await client.get(
                f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}"
            )
            print("✅ Realm configuration accessible")
            
    except Exception as e:
        print(f"❌ Keycloak connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_keycloak_connection())