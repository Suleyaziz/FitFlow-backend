from app import create_app
import requests
import json
import random

app = create_app()

def test_all_routes():
    """Test all API routes"""
    base_url = "http://localhost:5555"
    
    print("🚀 Testing All API Routes")
    print("=" * 50)
    
    # 1. Test main endpoint
    print("\n1. Testing main endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   GET / - Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Response: {response.json()}")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 2. Test authentication endpoints
    print("\n2. Testing authentication endpoints...")
    auth_endpoints = [
        ("POST", "/login", {"username": "fitfanatic", "password": "password123"}),
        ("POST", "/register", {"username": "route_test_user", "email": "route_test@example.com", "password": "test123"}),
        ("POST", "/users/login", {"username": "fitfanatic", "password": "password123"}),
        ("POST", "/users/register", {"username": "route_test_user2", "email": "route_test2@example.com", "password": "test123"})
    ]
    
    for method, endpoint, data in auth_endpoints:
        try:
            if method == "POST":
                response = requests.post(f"{base_url}{endpoint}", json=data)
            print(f"   {method} {endpoint} - Status: {response.status_code}")
            if response.status_code in [200, 201]:
                print(f"   ✅ Success")
            else:
                print(f"   ❌ Failed: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # 3. Test data endpoints (protected routes)
    print("\n3. Testing protected data endpoints...")
    
    # First get a token
    try:
        login_data = {"username": "fitfanatic", "password": "password123"}
        login_response = requests.post(f"{base_url}/login", json=login_data)
        
        if login_response.status_code == 200:
            token = login_response.json().get('token')
            print(f"   ✅ Got JWT token: {token[:50]}...")
            
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test protected endpoints
            protected_endpoints = [
                ("GET", "/users"),
                ("GET", "/workouts"),
                ("GET", "/exercises"),
                ("GET", "/progress_logs"),
                ("POST", "/workouts", {"name": "Test Workout", "duration": 30}),
                ("POST", "/exercises", {"name": f"Unique Test Exercise {random.randint(1000, 9999)}", "category": "Strength"})  # ← FIXED: Unique name
            ]
            
            for method, endpoint, *data in protected_endpoints:
                try:
                    if method == "GET":
                        response = requests.get(f"{base_url}{endpoint}", headers=headers)
                    elif method == "POST":
                        response = requests.post(f"{base_url}{endpoint}", json=data[0] if data else {}, headers=headers)
                    
                    print(f"   {method} {endpoint} - Status: {response.status_code}")
                    if response.status_code in [200, 201]:
                        print(f"   ✅ Success")
                    elif response.status_code == 401:
                        print(f"   🔒 Unauthorized (invalid token)")
                    else:
                        print(f"   ❌ Failed: {response.text}")
                except Exception as e:
                    print(f"   ❌ Error: {e}")
        else:
            print("   ❌ Could not get JWT token for protected routes test")
            
    except Exception as e:
        print(f"   ❌ Error testing protected routes: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Route testing completed!")

if __name__ == "__main__":
    test_all_routes()