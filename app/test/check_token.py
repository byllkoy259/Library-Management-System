import json
from jose import jwt
import datetime

def check_token_expiration(token):
    """
    Kiểm tra thời gian hết hạn của JWT token
    """
    try:
        # Decode payload không verify signature
        payload = jwt.get_unverified_claims(token)
        
        print("=" * 50)
        print("TOKEN EXPIRATION CHECK")
        print("=" * 50)
        
        # Lấy các thông tin thời gian
        issued_at = payload.get('iat')
        expires_at = payload.get('exp')
        not_before = payload.get('nbf')
        
        current_timestamp = datetime.datetime.now().timestamp()
        
        if issued_at:
            issued_time = datetime.datetime.fromtimestamp(issued_at)
            print(f"Token issued at: {issued_time}")
        
        if expires_at:
            exp_time = datetime.datetime.fromtimestamp(expires_at)
            current_time = datetime.datetime.now()
            
            print(f"Token expires at: {exp_time}")
            print(f"Current time:     {current_time}")
            
            # Tính thời gian còn lại
            time_remaining = exp_time - current_time
            
            if time_remaining.total_seconds() > 0:
                minutes_remaining = int(time_remaining.total_seconds() // 60)
                seconds_remaining = int(time_remaining.total_seconds() % 60)
                print(f"Time remaining: {minutes_remaining} minutes, {seconds_remaining} seconds")
                print("STATUS: ✅ TOKEN VALID")
            else:
                minutes_expired = int(abs(time_remaining.total_seconds()) // 60)
                seconds_expired = int(abs(time_remaining.total_seconds()) % 60)
                print(f"Expired {minutes_expired} minutes, {seconds_expired} seconds ago")
                print("STATUS: ❌ TOKEN EXPIRED")
        
        # Hiển thị thêm thông tin
        print("\nOther token info:")
        print(f"Subject: {payload.get('sub')}")
        print(f"Username: {payload.get('preferred_username')}")
        print(f"Email: {payload.get('email')}")
        print(f"Issuer: {payload.get('iss')}")
        print(f"Audience: {payload.get('aud')}")
        
        # Token lifetime
        if issued_at and expires_at:
            lifetime_seconds = expires_at - issued_at
            lifetime_minutes = lifetime_seconds // 60
            print(f"Token lifetime: {lifetime_minutes} minutes")
        
        print("=" * 50)
        
        return expires_at > current_timestamp if expires_at else None
        
    except Exception as e:
        print(f"Error checking token: {e}")
        return None

def main():
    print("JWT TOKEN EXPIRATION CHECKER")
    print("Enter your JWT token (paste and press Enter):")
    token = input().strip()
    
    if not token:
        print("No token provided")
        return
    
    is_valid = check_token_expiration(token)
    
    if is_valid is True:
        print("\n✅ Token is still valid - you can use it")
    elif is_valid is False:
        print("\n❌ Token has expired - get a new one")
    else:
        print("\n⚠️ Could not determine token status")

if __name__ == "__main__":
    main()