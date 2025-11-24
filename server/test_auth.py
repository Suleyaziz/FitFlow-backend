import requests
import json
import time

BASE_URL = "http://localhost:5555"

def test_auth_endpoints():
    print("=== Testing Authentication Endpoints ===\n")
    
    # Generate unique username to avoid conflicts
    timestamp = int(time.time())
    test_username = f"testuser{timestamp}"
    
    # Test 1: Register a new user
    register_data = {
        "username": test_username,
        "email": f"test{timestamp}@example.com",
        "password": "testpassword123",
        "age": 25,
        "height": 175.0,
        "weight": 70.0,
        "fitness_goal": "Get stronger"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"1. Register endpoint: {response.status_code}")
        if response.status_code == 201:
            token = response.json().get('token')
            print("   ✅ User registered successfully")
            print(f"   Token received: {token[:50]}...")
        else:
            print(f"   ❌ Failed: {response.text}")
            # If registration failed, try login with existing user
            test_username = "fitfanatic"
    except Exception as e:
        print(f"   ❌ Register endpoint failed: {e}")
        test_username = "fitfanatic"
    
    # Test 2: Login with the user
    login_data = {
        "username": test_username,
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"\n2. Login endpoint: {response.status_code}")
        if response.status_code == 200:
            token = response.json().get('token')
            user_data = response.json().get('user')
            print("   ✅ Login successful")
            print(f"   User: {user_data['username']}")
        else:
            print(f"   ❌ Failed: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Login endpoint failed: {e}")
        return
    
    # Test 3: Access protected route with token
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        print(f"\n3. Protected route: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Successfully accessed protected route")
            user_info = response.json().get('user')
            print(f"   User data: {user_info['username']}")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Protected route failed: {e}")
    
    # Test 4: Try protected route without token
    try:
        response = requests.get(f"{BASE_URL}/auth/me")
        print(f"\n4. No token test: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Correctly blocked access without token")
        else:
            print("   ❌ Should return 401 for missing token")
    except Exception as e:
        print(f"   ❌ No token test failed: {e}")
    
    # Test 5: Try protected route with invalid token
    try:
        headers_invalid = {"Authorization": "Bearer invalid.token.here"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers_invalid)
        print(f"\n5. Invalid token test: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Correctly blocked access with invalid token")
        else:
            print("   ❌ Should return 401 for invalid token")
    except Exception as e:
        print(f"   ❌ Invalid token test failed: {e}")

if __name__ == '__main__':
    test_auth_endpoints()