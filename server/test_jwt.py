from app import app, db
import time

def test_jwt_implementation():
    # Import inside function
    from models import User
    
    with app.app_context():
        print("=== Testing JWT Implementation ===\n")
        
        # Your test code remains the same...
        user = User.query.first()
        # Rest of your test code...

if __name__ == '__main__':
    test_jwt_implementation()