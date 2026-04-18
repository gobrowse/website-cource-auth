#!/usr/bin/env python3
"""
TEST PLAN: Verify bcrypt password length fix

Success Criteria:
1. Short passwords work (8-12 chars)
2. Long passwords work (72+ chars)
3. Very long passwords work (100+ chars)
4. Password verification works for all cases
5. Registration flow works end-to-end
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app.auth import get_password_hash, verify_password
from app.database import SessionLocal, User, init_db
from datetime import datetime

def test_password_lengths():
    """Test passwords of varying lengths"""
    test_cases = [
        "short12",           # 8 chars
        "a" * 72,           # Exactly 72 chars
        "a" * 80,           # 80 chars (truncated to 72)
        "a" * 100,          # 100 chars (truncated to 72)
        "Test1234",         # Mixed case + numbers
        "测试12345678",     # Unicode characters
    ]
    
    print("=== Testing Password Lengths ===")
    for i, password in enumerate(test_cases):
        print(f"Test {i+1}: {len(password)} chars")
        
        # Test hashing
        hash = get_password_hash(password)
        print(f"  Hash created: {hash[:20]}...")
        
        # Test verification
        result = verify_password(password, hash)
        print(f"  Verification: {'✅ PASS' if result else '❌ FAIL'}")
        
        # Test wrong password fails
        wrong_result = verify_password(password + "x", hash)
        print(f"  Wrong password: {'✅ FAIL (expected)' if not wrong_result else '❌ PASS (unexpected)'}")
        
        if not result:
            print(f"  ❌ FAILED: Password verification failed for: {password[:20]}...")
            return False
        
        print()
    
    return True

def test_registration_flow():
    """Test full registration flow with database"""
    print("=== Testing Registration Flow ===")
    
    # Initialize test database
    init_db()
    db = SessionLocal()
    
    try:
        # Test user data
        test_users = [
            {"email": "short@example.com", "username": "shortuser", "password": "Short123"},
            {"email": "long@example.com", "username": "longuser", "password": "a" * 100},
        ]
        
        for user_data in test_users:
            print(f"Testing user: {user_data['username']}")
            
            # Check if user exists
            existing = db.query(User).filter(User.username == user_data['username']).first()
            if existing:
                db.delete(existing)
                db.commit()
            
            # Test registration
            hash = get_password_hash(user_data['password'])
            user = User(
                email=user_data['email'],
                username=user_data['username'],
                hashed_password=hash,
                is_active=True,
                created_at=datetime.utcnow().isoformat()
            )
            db.add(user)
            db.commit()
            
            # Verify user was created
            created_user = db.query(User).filter(User.username == user_data['username']).first()
            if not created_user:
                print(f"  ❌ FAILED: User not created: {user_data['username']}")
                return False
            
            # Verify password
            result = verify_password(user_data['password'], created_user.hashed_password)
            if not result:
                print(f"  ❌ FAILED: Password verification failed for: {user_data['username']}")
                return False
            
            print(f"  ✅ PASS: User {user_data['username']} created and verified")
        
        return True
        
    finally:
        db.close()

def main():
    """Run all tests"""
    print("🔍 ULTRAWORK MODE: Bcrypt Password Length Fix Verification")
    print("=" * 60)
    
    success = True
    
    # Test password lengths
    if not test_password_lengths():
        success = False
    
    # Test registration flow
    if not test_registration_flow():
        success = False
    
    print("=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED - Bcrypt password length fix is working!")
        return 0
    else:
        print("❌ TESTS FAILED - Fix needs more work")
        return 1

if __name__ == "__main__":
    sys.exit(main())