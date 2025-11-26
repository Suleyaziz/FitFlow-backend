from app import app, db
from models import User, Workout, Exercise, WorkoutExercise, ProgressLog
from datetime import datetime, timedelta
import random

def clear_data():
    """Clear existing data from all tables"""
    print("Clearing existing data...")
    db.session.query(WorkoutExercise).delete()
    db.session.query(ProgressLog).delete()
    db.session.query(Workout).delete()
    db.session.query(Exercise).delete()
    db.session.query(User).delete()
    db.session.commit()

def create_exercises():
    """Create exercise library"""
    print("Creating exercise library...")
    
    exercises = [
        # Cardio exercises
        Exercise(name="Running", category="Cardio", muscle_group="Full Body", equipment="None", difficulty="Beginner", calories_per_minute=10.0),
        Exercise(name="Cycling", category="Cardio", muscle_group="Legs", equipment="Bicycle", difficulty="Beginner", calories_per_minute=8.5),
        Exercise(name="Jump Rope", category="Cardio", muscle_group="Full Body", equipment="Jump Rope", difficulty="Intermediate", calories_per_minute=12.0),
        
        # Strength exercises
        Exercise(name="Push-ups", category="Strength", muscle_group="Chest", equipment="None", difficulty="Beginner", calories_per_minute=7.0),
        Exercise(name="Squats", category="Strength", muscle_group="Legs", equipment="None", difficulty="Beginner", calories_per_minute=6.5),
        Exercise(name="Dumbbell Curls", category="Strength", muscle_group="Biceps", equipment="Dumbbells", difficulty="Beginner", calories_per_minute=5.0),
        Exercise(name="Bench Press", category="Strength", muscle_group="Chest", equipment="Barbell", difficulty="Intermediate", calories_per_minute=8.0),
        Exercise(name="Deadlift", category="Strength", muscle_group="Back", equipment="Barbell", difficulty="Advanced", calories_per_minute=9.0),
        
        # Flexibility exercises
        Exercise(name="Sun Salutation", category="Flexibility", muscle_group="Full Body", equipment="Yoga Mat", difficulty="Beginner", calories_per_minute=3.0),
        Exercise(name="Hamstring Stretch", category="Flexibility", muscle_group="Legs", equipment="None", difficulty="Beginner", calories_per_minute=2.5)
    ]
    
    db.session.add_all(exercises)
    db.session.commit()
    return exercises

def create_users():
    """Create sample users"""
    print("Creating users...")
    
    users = [
        User(username="fitfanatic", email="fitfanatic@example.com", age=28, height=175.0, weight=70.0, fitness_goal="Build muscle", target_weight=75.0, experience_level="Intermediate"),
        User(username="cardioqueen", email="cardioqueen@example.com", age=32, height=165.0, weight=60.0, fitness_goal="Improve endurance", target_weight=58.0, experience_level="Beginner"),
        User(username="yogamaster", email="yogamaster@example.com", age=45, height=170.0, weight=65.0, fitness_goal="Increase flexibility", target_weight=65.0, experience_level="Advanced")
    ]
    
    # Set passwords for all users
    for user in users:
        user.set_password("password123")
    
    db.session.add_all(users)
    db.session.commit()
    return users

def create_workouts(users, exercises):
    """Create sample workouts"""
    print("Creating workouts...")
    
    workouts = []
    workout_date = datetime.now().date()
    
    # User 1: Strength workouts
    workouts.append(Workout(user_id=users[0].id, name="Upper Body Strength", date=workout_date - timedelta(days=2), duration=45, calories_burned=320, workout_type="Strength"))
    workouts.append(Workout(user_id=users[0].id, name="Leg Day", date=workout_date - timedelta(days=4), duration=60, calories_burned=450, workout_type="Strength"))
    
    # User 2: Cardio workouts
    workouts.append(Workout(user_id=users[1].id, name="Morning Run", date=workout_date - timedelta(days=1), duration=30, calories_burned=300, workout_type="Cardio"))
    workouts.append(Workout(user_id=users[1].id, name="HIIT Session", date=workout_date - timedelta(days=3), duration=25, calories_burned=280, workout_type="HIIT"))
    
    # User 3: Flexibility workouts
    workouts.append(Workout(user_id=users[2].id, name="Morning Yoga", date=workout_date, duration=40, calories_burned=180, workout_type="Yoga"))
    
    db.session.add_all(workouts)
    db.session.commit()
    return workouts

def create_workout_exercises(workouts, exercises, users):
    """Create workout exercise entries"""
    print("Creating workout exercises...")
    
    workout_exercises = []
    
    # Workout 1: Upper Body Strength
    workout_exercises.append(WorkoutExercise(user_id=users[0].id, workout_id=workouts[0].id, exercise_id=exercises[3].id, sets=3, reps=15, order=1))
    workout_exercises.append(WorkoutExercise(user_id=users[0].id, workout_id=workouts[0].id, exercise_id=exercises[5].id, sets=3, reps=12, weight=12.5, order=2))
    workout_exercises.append(WorkoutExercise(user_id=users[0].id, workout_id=workouts[0].id, exercise_id=exercises[6].id, sets=4, reps=8, weight=60.0, order=3))
    
    # Workout 2: Leg Day
    workout_exercises.append(WorkoutExercise(user_id=users[0].id, workout_id=workouts[1].id, exercise_id=exercises[4].id, sets=4, reps=10, weight=80.0, order=1))
    workout_exercises.append(WorkoutExercise(user_id=users[0].id, workout_id=workouts[1].id, exercise_id=exercises[7].id, sets=3, reps=6, weight=100.0, order=2))
    
    # Workout 3: Morning Run
    workout_exercises.append(WorkoutExercise(user_id=users[1].id, workout_id=workouts[2].id, exercise_id=exercises[0].id, duration=1800, distance=5.0, calories_burned=300, order=1))
    
    # Workout 4: HIIT Session
    workout_exercises.append(WorkoutExercise(user_id=users[1].id, workout_id=workouts[3].id, exercise_id=exercises[2].id, duration=900, calories_burned=180, order=1))
    workout_exercises.append(WorkoutExercise(user_id=users[1].id, workout_id=workouts[3].id, exercise_id=exercises[3].id, sets=3, reps=10, order=2))
    
    # Workout 5: Morning Yoga
    workout_exercises.append(WorkoutExercise(user_id=users[2].id, workout_id=workouts[4].id, exercise_id=exercises[8].id, duration=2400, calories_burned=180, order=1))
    
    db.session.add_all(workout_exercises)
    db.session.commit()
    return workout_exercises

def create_progress_logs(users):
    """Create sample progress logs"""
    print("Creating progress logs...")
    
    progress_logs = []
    base_date = datetime.now().date()
    
    # User 1 progress logs
    for i in range(4):
        progress_logs.append(ProgressLog(user_id=users[0].id, log_date=base_date - timedelta(weeks=i), weight=70.0 - (i * 0.5), chest=95.0 + (i * 0.5), waist=80.0 - (i * 1.0), biceps=32.0 + (i * 0.3), energy_level=8, mood="Great"))
    
    # User 2 progress logs
    for i in range(4):
        progress_logs.append(ProgressLog(user_id=users[1].id, log_date=base_date - timedelta(weeks=i), weight=60.0 - (i * 0.8), waist=70.0 - (i * 1.2), hips=95.0 - (i * 0.8), energy_level=7, mood="Good"))
    
    # User 3 progress logs
    for i in range(4):
        progress_logs.append(ProgressLog(user_id=users[2].id, log_date=base_date - timedelta(weeks=i), weight=65.0, energy_level=9, mood="Great"))
    
    db.session.add_all(progress_logs)
    db.session.commit()
    return progress_logs

if __name__ == '__main__':
    with app.app_context():
        print("Starting FitFlow database seeding...")
        clear_data()
        exercises = create_exercises()
        users = create_users()
        workouts = create_workouts(users, exercises)
        workout_exercises = create_workout_exercises(workouts, exercises, users)
        progress_logs = create_progress_logs(users)
        print("FitFlow database seeded successfully!")
        print(f"Created: {len(users)} users, {len(exercises)} exercises, {len(workouts)} workouts, {len(workout_exercises)} workout exercises, {len(progress_logs)} progress logs")