#!/usr/bin/env python3
"""
DEBUG TOKEN VERIFICATION

Investigate why token verification is failing.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app.auth import create_access_token
from jose import jwt
from app.database import SECRET_KEY, ALGORITHM

def debug_token():
    """Debug token creation and verification"""
    print("🔍 DEBUGGING TOKEN VERIFICATION")
    print("=" * 40)
    
    # Create token
    username = "testuser"
    token = create_access_token(data={"sub": username})
    
    print(f"🔑 Token: {token}")
    
    try:
        # Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"✅ Token decoded successfully")
        print(f"📋 Payload: {payload}")
        
        # Check fields
        username_from_token = payload.get("sub")
        exp = payload.get("exp")
        
        print(f"👤 Username from token: {username_from_token}")
        print(f"⏰ Expiration: {exp}")
        
        if username_from_token == username:
            print("✅ Username matches")
        else:
            print("❌ Username mismatch")
            
        # Check if token is expired
        import time
        if exp and exp < time.time():
            print("❌ Token expired")
        else:
            print("✅ Token not expired")
            
        return True
        
    except Exception as e:
        print(f"❌ Token decode failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_token()
    sys.exit(0 if success else 1)