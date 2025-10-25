import httpx
import asyncio
from jose import jwt
import json

async def test_keycloak_data():
    print("=" * 60)
    print("TESTING KEYCLOAK INTEGRATION")
    print("=" * 60)
    
    # 1. Test JWKS endpoint
    print("\n1. FETCHING JWKS...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://127.0.0.1:8080/realms/library-realm/protocol/openid-connect/certs"
            )
            if response.status_code == 200:
                jwks = response.json()
                print(f"✅ JWKS fetched successfully!")
                print(f"📊 Number of keys: {len(jwks['keys'])}")
                
                for i, key in enumerate(jwks['keys']):
                    print(f"\n🔑 Key {i+1}:")
                    print(f"   ID (kid): {key.get('kid')}")
                    print(f"   Type: {key.get('kty')}")
                    print(f"   Use: {key.get('use')}")
                    print(f"   Algorithm: {key.get('alg', 'N/A')}")
            else:
                print(f"❌ Failed to fetch JWKS: {response.status_code}")
                print(f"Response: {response.text}")
                return
                
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Check if Keycloak is running and realm exists")
        return
    
    # 2. Test token endpoint
    print("\n2. TESTING TOKEN...")
    username = input("Enter Keycloak username: ").strip()
    password = input("Enter Keycloak password: ").strip()
    
    if not username or not password:
        print("❌ Username or password is empty")
        return
    
    try:
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                "http://127.0.0.1:8080/realms/library-realm/protocol/openid-connect/token",
                data={
                    "grant_type": "password",
                    "client_id": "fastapi-keycloak",
                    "client_secret": "Tl70vjSesGPGY5eF0IhOuJStIohjUEYd",
                    "username": username,
                    "password": password,
                }
            )
            
            if token_response.status_code == 200:
                token_data = token_response.json()
                access_token = token_data["access_token"]
                print("✅ Token received!")
                
                # Decode JWT header
                header = jwt.get_unverified_header(access_token)
                print(f"\n📋 JWT Header:")
                print(f"   Algorithm: {header.get('alg')}")
                print(f"   Type: {header.get('typ')}")
                print(f"   Key ID: {header.get('kid')}")
                
                # Decode payload
                payload = jwt.get_unverified_claims(access_token)
                print(f"\n📋 JWT Payload (key info):")
                print(f"   Subject: {payload.get('sub')}")
                print(f"   Username: {payload.get('preferred_username')}")
                print(f"   Email: {payload.get('email')}")
                
                # Check kid matching
                token_kid = header.get('kid')
                matching_key = None
                for key in jwks['keys']:
                    if key.get('kid') == token_kid:
                        matching_key = key
                        break
                
                if matching_key:
                    print(f"\n✅ Found matching key in JWKS!")
                    print(f"   Key ID: {matching_key['kid']}")
                    print(f"   Key Type: {matching_key['kty']}")
                else:
                    print(f"\n❌ No matching key found!")
                    available_kids = [k.get('kid') for k in jwks['keys']]
                    print(f"   Token kid: {token_kid}")
                    print(f"   Available kids: {available_kids}")
                    
            else:
                print(f"❌ Failed to get token: {token_response.status_code}")
                print(f"Response: {token_response.text}")
                
    except Exception as e:
        print(f"❌ Error getting token: {e}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_keycloak_data())