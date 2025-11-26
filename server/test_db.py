from app import app, db

def test_database():
    # Import models inside the function to avoid circular imports
    from models import User, Workout, Exercise, WorkoutExercise, ProgressLog
    
    with app.app_context():
        print("=== FitFlow Database Test ===\n")
        
        # Test code remains the same...
        print("1. Record Counts:")
        print(f"   Users: {User.query.count()}")
        print(f"   Workouts: {Workout.query.count()}")
        print(f"   Exercises: {Exercise.query.count()}")
        print(f"   Workout Exercises: {WorkoutExercise.query.count()}")
        print(f"   Progress Logs: {ProgressLog.query.count()}\n")
        
        # Rest of your test code...

if __name__ == '__main__':
    test_database()