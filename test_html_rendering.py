#!/usr/bin/env python3
"""
TEST: Verify HTML is properly rendered (not shown as raw text)

This test verifies that FastAPI returns proper HTMLResponse
objects with correct Content-Type headers.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app.main import app
from fastapi.testclient import TestClient

# Create test client
client = TestClient(app)

print("🔍 TESTING HTML RENDERING FIX")
print("=" * 60)

# Test 1: Login GET - should return HTMLResponse
print("\n📋 Test 1: GET /login")
response = client.get('/login')
print(f"Status: {response.status_code}")
print(f"Content-Type: {response.headers.get('content-type')}")
print(f"✅ PASS" if 'text/html' in response.headers.get('content-type', '') else "❌ FAIL")

# Test 2: Register GET - should return HTMLResponse
print("\n📋 Test 2: GET /register")
response = client.get('/register')
print(f"Status: {response.status_code}")
print(f"Content-Type: {response.headers.get('content-type')}")
print(f"✅ PASS" if 'text/html' in response.headers.get('content-type', '') else "❌ FAIL")

# Test 3: Login POST with invalid credentials - should return HTMLResponse (not raw HTML)
print("\n📋 Test 3: POST /login (invalid credentials)")
response = client.post('/login', data={'username': 'nonexistent', 'password': 'wrong'})
print(f"Status: {response.status_code}")
print(f"Content-Type: {response.headers.get('content-type')}")
print(f"Response preview: {response.text[:100]}...")
print(f"✅ PASS - Returns HTMLResponse" if 'text/html' in response.headers.get('content-type', '') else "❌ FAIL")

# Test 4: Register POST with existing user - should return HTMLResponse
print("\n📋 Test 4: POST /register (existing user)")
response = client.post('/register', data={'email': 'test@example.com', 'username': 'testuser', 'password': 'Test1234'})
print(f"Status: {response.status_code}")
print(f"Content-Type: {response.headers.get('content-type')}")
print(f"✅ PASS - Returns HTMLResponse" if 'text/html' in response.headers.get('content-type', '') else "❌ FAIL")

print("\n" + "=" * 60)
print("🎉 ALL TESTS COMPLETED")
print("\nIf all tests show 'text/html' Content-Type, the HTML rendering issue is FIXED!")
print("The browser will now render HTML instead of displaying it as text.")