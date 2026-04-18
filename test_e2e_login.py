#!/usr/bin/env python3
"""
END-TO-END LOGIN TEST

Test the complete login flow from registration to course access.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

import requests
import time
import subprocess
import signal
import atexit

def start_server():
    """Start the FastAPI server in the background"""
    print("🚀 Starting server...")
    server = subprocess.Popen(
        ['uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8003'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    # Register cleanup
    def cleanup():
        print("🛑 Stopping server...")
        os.killpg(os.getpgid(server.pid), signal.SIGTERM)
    atexit.register(cleanup)
    
    # Wait for server to start
    time.sleep(3)
    return server

def test_e2e_login():
    """Test end-to-end login flow"""
    print("🔍 TESTING END-TO-END LOGIN FLOW")
    print("=" * 50)
    
    try:
        # Test 1: Check if server is running
        print("🌐 Testing server availability...")
        response = requests.get('http://localhost:8003/', timeout=5)
        print(f"✅ Home page: {response.status_code}")
        
        # Test 2: Register new user
        print("\n📝 Testing registration...")
        response = requests.post(
            'http://localhost:8003/register',
            data={
                'email': 'e2e_test@example.com',
                'username': 'e2etest',
                'password': 'Test1234'
            },
            allow_redirects=False,
            timeout=5
        )
        
        if response.status_code == 302 and '/login?registered=true' in response.headers.get('Location', ''):
            print("✅ Registration: PASS (redirect to login)")
        else:
            print(f"❌ Registration: FAIL - Status: {response.status_code}, Location: {response.headers.get('Location')}")
            return False
        
        # Test 3: Login
        print("\n🔐 Testing login...")
        response = requests.post(
            'http://localhost:8003/login',
            data={
                'username': 'e2etest',
                'password': 'Test1234'
            },
            allow_redirects=False,
            timeout=5
        )
        
        if response.status_code == 302 and '/courses' in response.headers.get('Location', ''):
            print("✅ Login: PASS (redirect to courses)")
            print(f"🍪 Cookies: {response.cookies.get('access_token', 'Not set')}")
        else:
            print(f"❌ Login: FAIL - Status: {response.status_code}, Location: {response.headers.get('Location')}")
            return False
        
        # Test 4: Access courses page (with cookie)
        print("\n📚 Testing course access...")
        response = requests.get(
            'http://localhost:8003/courses',
            cookies=response.cookies,
            timeout=5
        )
        
        if response.status_code == 200 and 'My Courses' in response.text:
            print("✅ Course access: PASS")
        else:
            print(f"❌ Course access: FAIL - Status: {response.status_code}")
            print(f"Response preview: {response.text[:100]}...")
            return False
        
        print("\n🎉 END-TO-END TEST PASSED!")
        print("✅ Login redirects to courses page correctly")
        print("✅ Courses are accessible after login")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Run the end-to-end test"""
    server = start_server()
    
    try:
        success = test_e2e_login()
        return 0 if success else 1
    finally:
        # Cleanup
        os.killpg(os.getpgid(server.pid), signal.SIGTERM)

if __name__ == "__main__":
    sys.exit(main())