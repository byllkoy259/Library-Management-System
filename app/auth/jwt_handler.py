import base64
from fastapi import HTTPException, status
import httpx
from jose import JWTError, jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from app.config import settings

_jwks_cache = None

# Hàm lấy JWKS từ Keycloak
async def get_jwks():
    global _jwks_cache
    if _jwks_cache is None:    
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs")
                response.raise_for_status() # Kiểm tra lỗi HTTP
                jwks = response.json()
                print(f"JWKS fetched: {len(jwks.get('keys', []))} keys")
                _jwks_cache = jwks
                return jwks
            except httpx.HTTPError as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to fetch JWKS from Keycloak: {str(e)}"
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error processing JWKS: {str(e)}"
                )
    return _jwks_cache


# Chuyển đổi JWK sang định dạng RSA
def jwk_to_rsa_key(jwk):
    try:
        n = jwk['n']
        e = jwk['e']

        # Add padding for base64 decoding
        n += '=' * (4 - len(n) % 4)
        e += '=' * (4 - len(e) % 4)

        # Decode base64url
        n_bytes = base64.urlsafe_b64decode(n)
        e_bytes = base64.urlsafe_b64decode(e)

        # Convert bytes to integers
        n_int = int.from_bytes(n_bytes, byteorder='big')
        e_int = int.from_bytes(e_bytes, byteorder='big')
        
        # Create RSA public key
        public_numbers = rsa.RSAPublicNumbers(e_int, n_int)
        public_key = public_numbers.public_key()
        
        # Convert to PEM format
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Invalid JWK: {e}")
    

# Hàm xác minh token
async def verify_token(token: str):
    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        if not kid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token header: 'kid' missing",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        jwks = await get_jwks()

        if not jwks or "keys" not in jwks:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="JWKS not available",
                headers={"WWW-Authenticate": "Bearer"},
            )

        rsa_key = None
        for key in jwks["keys"]:
            if (key["kid"] == kid and key["kty"] == "RSA" and key["use"] == "sig"):
                rsa_key = jwk_to_rsa_key(key)
                break
        
        if rsa_key is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to find appropriate key",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=settings.KEYCLOAK_CLIENT_ID,
            options={"verify_signature": True, "verify_exp": True, "verify_aud": False}  # Có thể tắt verify_aud nếu không sử dụng
        )

        print(f"Token audience: {payload.get('aud')}")
        print(f"Expected client ID: {settings.KEYCLOAK_CLIENT_ID}")
        
        return payload
    
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
            

def get_user_info(payload: dict):
    return {
        "sub": payload.get("sub"),
        "username": payload.get("preferred_username"),
        "email": payload.get("email"),
        "full_name": payload.get("name"),
        "roles": payload.get("realm_access", {}).get("roles", [])
    }