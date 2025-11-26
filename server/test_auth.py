import requests
import json
import time

BASE_URL = "http://localhost:5555"

def test_auth_endpoints():
    print("=== Testing Authentication Endpoints ===\n")
    
    # Test 1: Try to login with one of the seeded users
    # These should exist from your seed.py
    test_users = [
        {"username": "fitfanatic", "password": "password123"},
        {"username": "cardioqueen", "password": "password123"}, 
        {"username": "yogamaster", "password": "password123"}
    ]
    
    token = None
    
    for user_data in test_users:
        try:
            print(f"1. Trying login with: {user_data['username']}")
            response = requests.post(f"{BASE_URL}/auth/login", json=user_data)
            print(f"   Login response: {response.status_code}")
            
            if response.status_code == 200:
                token = response.json().get('token')
                user_info = response.json().get('user')
                print(f"   ✅ Login successful!")
                print(f"   User: {user_info['username']}")
                print(f"   Token: {token[:50]}...")
                break
            else:
                print(f"   ❌ Failed: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Login failed: {e}")
    
    if not token:
        print("\n💡 All logins failed. Let's try registering a new user...")
        
        # Test 2: Register a new user
        timestamp = int(time.time())
        register_data = {
            "username": f"testuser{timestamp}",
            "email": f"test{timestamp}@example.com",
            "password": "testpassword123",
            "age": 25,
            "height": 175.0,
            "weight": 70.0,
            "fitness_goal": "Test fitness goal"
        }
        
        try:
            response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
            print(f"\n2. Register endpoint: {response.status_code}")
            if response.status_code == 201:
                token = response.json().get('token')
                print("   ✅ User registered successfully")
                print(f"   Token: {token[:50]}...")
            else:
                print(f"   ❌ Registration failed: {response.text}")
                return
        except Exception as e:
            print(f"   ❌ Registration failed: {e}")
            return
    
    # Test 3: Access protected route with token
    if token:
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