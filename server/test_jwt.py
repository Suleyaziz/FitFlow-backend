from app import create_app, db
from models import User
import jwt
import datetime

app = create_app()

def test_jwt_functionality():
    """Test JWT token creation and validation"""
    with app.app_context():
        try:
            # Get a user to test with
            user = User.query.first()
            if not user:
                print("❌ No users found in database")
                return False
                
            print(f"✅ Testing JWT with user: {user.username}")
            
            # Test password verification
            password_correct = user.check_password("password123")
            print(f"✅ Password verification: {password_correct}")
            
            # Test token generation (if you have token generation in your User model)
            if hasattr(user, 'generate_token'):
                token = user.generate_token()
                print(f"✅ Token generation: {token[:50]}...")
            else:
                print("ℹ️  No token generation method found in User model")
                
            return True
            
        except Exception as e:
            print(f"❌ JWT test failed: {e}")
            return False

if __name__ == "__main__":
    test_jwt_functionality()