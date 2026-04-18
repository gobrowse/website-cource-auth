#!/usr/bin/env python3
"""
DEBUG LOGIN FLOW

Test the login flow step by step to identify where it fails.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app.database import SessionLocal, User, init_db
from app.auth import get_password_hash, verify_password, create_access_token
from datetime import datetime

def test_login_flow():
    """Test the complete login flow"""
    print("🔍 DEBUGGING LOGIN FLOW")
    print("=" * 40)
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    try:
        # Create test user if not exists
        test_user = db.query(User).filter(User.username == "testuser").first()
        if not test_user:
            print("📝 Creating test user...")
            hashed_password = get_password_hash("Test1234")
            test_user = User(
                email="test@example.com",
                username="testuser",
                hashed_password=hashed_password,
                is_active=True,
                created_at=datetime.utcnow().isoformat()
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            print("✅ Test user created")
        else:
            print("👤 Using existing test user")
        
        # Test 1: Verify credentials
        print("\n🔐 Testing credential verification...")
        result = verify_password("Test1234", test_user.hashed_password)
        print(f"✅ Password verification: {'PASS' if result else 'FAIL'}")
        
        if not result:
            print("❌ Password verification failed!")
            return False
        
        # Test 2: Create token
        print("\n🔑 Testing token creation...")
        token = create_access_token(data={"sub": test_user.username})
        print(f"✅ Token created: {token[:20]}...")
        
        # Test 3: Verify token
        print("\n🔍 Testing token verification...")
        from app.auth import get_current_user
        from fastapi import Request
        
        # Mock request with token
        class MockRequest:
            def __init__(self, token):
                self.cookies = {"access_token": token}
        
        mock_request = MockRequest(token)
        current_user = get_current_user(mock_request, db)
        
        if current_user and current_user.username == test_user.username:
            print("✅ Token verification: PASS")
        else:
            print("❌ Token verification: FAIL")
            return False
        
        print("\n🎉 ALL LOGIN TESTS PASSED!")
        print("The login flow should work correctly.")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = test_login_flow()
    sys.exit(0 if success else 1)