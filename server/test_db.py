from app import create_app, db
from models import User, Workout, Exercise

app = create_app()

def test_database_connection():
    """Test database connection and basic operations"""
    with app.app_context():
        try:
            # Test User model
            user_count = User.query.count()
            print(f"✅ Database connection successful")
            print(f"✅ Users in database: {user_count}")
            
            # Test Exercise model
            exercise_count = Exercise.query.count()
            print(f"✅ Exercises in database: {exercise_count}")
            
            # Test Workout model
            workout_count = Workout.query.count()
            print(f"✅ Workouts in database: {workout_count}")
            
            return True
            
        except Exception as e:
            print(f"❌ Database test failed: {e}")
            return False

if __name__ == "__main__":
    test_database_connection()