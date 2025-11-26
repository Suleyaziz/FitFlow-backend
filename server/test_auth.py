from app import create_app
import requests
import json
import random

app = create_app()

def test_auth_endpoints():
    """Test authentication endpoints"""
    base_url = "http://localhost:5555"
    
    print("=== Testing Authentication Endpoints ===")
    
    # Test login with seeded users
    test_users = [
        {"username": "fitfanatic", "password": "password123"},
        {"username": "cardioqueen", "password": "password123"},
        {"username": "yogamaster", "password": "password123"}
    ]
    
    for i, user in enumerate(test_users, 1):
        print(f"\n{i}. Trying login with: {user['username']}")
        try:
            # Try login endpoint
            login_response = requests.post(f"{base_url}/login", json=user)
            print(f"   Login response: {login_response.status_code}")
            
            if login_response.status_code == 200:
                token_data = login_response.json()
                print(f"   ✅ Login successful!")
                print(f"   Full response: {token_data}")
                
                # Get the token (it's called "token" in your response)
                token = token_data.get('token')
                if token:
                    print(f"   Token: {token[:50]}...")
                else:
                    print(f"   ❌ No token found. Available fields: {list(token_data.keys())}")
            else:
                print(f"   ❌ Failed: {login_response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection failed - is the server running on {base_url}?")
            return False
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test registration with unique user data
    print(f"\n2. Testing user registration...")
    try:
        # Generate unique username and email to avoid conflicts
        random_id = random.randint(1000, 9999)
        new_user = {
            "username": f"newuser{random_id}",
            "email": f"newuser{random_id}@example.com",
            "password": "testpass123",
            "age": 25,
            "height": 170.0,
            "weight": 65.0
        }
        
        # Try different registration endpoints
        endpoints = ["/register", "/users/register"]
        
        for endpoint in endpoints:
            reg_response = requests.post(f"{base_url}{endpoint}", json=new_user)
            print(f"   {endpoint} response: {reg_response.status_code}")
            
            if reg_response.status_code in [200, 201]:
                print(f"   ✅ Registration successful via {endpoint}!")
                break
            else:
                print(f"   ❌ Registration failed via {endpoint}: {reg_response.text}")
                
    except Exception as e:
        print(f"   ❌ Registration test error: {e}")
    
    return True

if __name__ == "__main__":
    test_auth_endpoints()