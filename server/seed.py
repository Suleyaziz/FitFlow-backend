#!/usr/bin/env python3

from app import app, db
from models import User, Workout, Exercise, WorkoutExercise, ProgressLog
from datetime import datetime, timedelta
import random

def clear_database():
    """Clear existing data from all tables"""
    print("Clearing existing data...")
    with app.app_context():
        WorkoutExercise.query.delete()
        Workout.query.delete()
        Exercise.query.delete()
        ProgressLog.query.delete()
        User.query.delete()
        db.session.commit()

def create_users():
    """Create sample users"""
    print("Creating users...")
    
    users = [
        User(
            username='fitfanatic',
            email='fitfanatic@example.com',
            age=28,
            height=175.0,
            weight=75.0,
            fitness_goal='Build muscle and increase strength',
            target_weight=80.0
        ),
        User(
            username='cardioqueen',
            email='cardioqueen@example.com',
            age=32,
            height=165.0,
            weight=62.0,
            fitness_goal='Lose weight and improve cardio endurance',
            target_weight=58.0
        ),
        User(
            username='gymwarrior',
            email='gymwarrior@example.com',
            age=25,
            height=180.0,
            weight=85.0,
            fitness_goal='Maintain current fitness level and improve flexibility',
            target_weight=85.0
        )
    ]
    
    # Set passwords for all users
    for user in users:
        user.set_password('password123')
    
    db.session.add_all(users)
    db.session.commit()
    return users

def create_exercises():
    """Create exercise library"""
    print("Creating exercises...")
    
    exercises = [
        # Strength exercises
        Exercise(name='Bench Press', category='Strength', muscle_group='Chest'),
        Exercise(name='Squats', category='Strength', muscle_group='Legs'),
        Exercise(name='Deadlifts', category='Strength', muscle_group='Back'),
        Exercise(name='Shoulder Press', category='Strength', muscle_group='Shoulders'),
        Exercise(name='Bicep Curls', category='Strength', muscle_group='Biceps'),
        Exercise(name='Tricep Extensions', category='Strength', muscle_group='Triceps'),
        Exercise(name='Pull-ups', category='Strength', muscle_group='Back'),
        Exercise(name='Lunges', category='Strength', muscle_group='Legs'),
        Exercise(name='Push-ups', category='Strength', muscle_group='Chest'),
        Exercise(name='Plank', category='Strength', muscle_group='Core'),
        
        # Cardio exercises
        Exercise(name='Running', category='Cardio', muscle_group='Full Body'),
        Exercise(name='Cycling', category='Cardio', muscle_group='Legs'),
        Exercise(name='Swimming', category='Cardio', muscle_group='Full Body'),
        Exercise(name='Jump Rope', category='Cardio', muscle_group='Full Body'),
        Exercise(name='Rowing', category='Cardio', muscle_group='Full Body'),
        Exercise(name='Elliptical', category='Cardio', muscle_group='Full Body'),
        
        # Flexibility exercises
        Exercise(name='Yoga Flow', category='Flexibility', muscle_group='Full Body'),
        Exercise(name='Stretching', category='Flexibility', muscle_group='Full Body'),
        Exercise(name='Pilates', category='Flexibility', muscle_group='Core')
    ]
    
    db.session.add_all(exercises)
    db.session.commit()
    return exercises

def create_workouts_and_exercises(users, exercises):
    """Create workouts and link exercises through WorkoutExercise"""
    print("Creating workouts and exercises...")
    
    workout_templates = [
        {
            'name': 'Upper Body Strength',
            'description': 'Focus on chest, shoulders, and arms',
            'exercises': ['Bench Press', 'Shoulder Press', 'Bicep Curls', 'Tricep Extensions']
        },
        {
            'name': 'Lower Body Power',
            'description': 'Leg day focusing on compound movements',
            'exercises': ['Squats', 'Deadlifts', 'Lunges']
        },
        {
            'name': 'Full Body Circuit',
            'description': 'Complete body workout circuit',
            'exercises': ['Push-ups', 'Squats', 'Pull-ups', 'Plank']
        },
        {
            'name': 'Cardio Blast',
            'description': 'High-intensity cardio session',
            'exercises': ['Running', 'Jump Rope', 'Cycling']
        },
        {
            'name': 'Active Recovery',
            'description': 'Light workout for recovery day',
            'exercises': ['Yoga Flow', 'Stretching', 'Swimming']
        }
    ]
    
    all_workouts = []
    
    for user in users:
        for i, template in enumerate(workout_templates):
            workout_date = datetime.now().date() - timedelta(days=random.randint(0, 30))
            
            workout = Workout(
                user_id=user.id,
                name=f"{template['name']} Session",
                description=template['description'],
                date=workout_date,
                duration=random.randint(30, 90),
                calories_burned=random.randint(200, 600)
            )
            
            db.session.add(workout)
            db.session.commit()
            all_workouts.append(workout)
            
            # Add exercises to workout through WorkoutExercise
            for order, exercise_name in enumerate(template['exercises']):
                exercise = next(ex for ex in exercises if ex.name == exercise_name)
                
                workout_exercise = WorkoutExercise(
                    user_id=user.id,
                    workout_id=workout.id,
                    exercise_id=exercise.id,
                    order=order + 1
                )
                
                # Add exercise-specific data
                if exercise.category == 'Strength':
                    workout_exercise.sets = random.randint(3, 5)
                    workout_exercise.reps = random.randint(8, 15)
                    workout_exercise.weight = random.randint(20, 100)
                elif exercise.category == 'Cardio':
                    workout_exercise.duration = random.randint(600, 1800)
                    if exercise.name == 'Running' or exercise.name == 'Cycling':
                        workout_exercise.distance = random.uniform(2.0, 10.0)
                
                workout_exercise.notes = f"Completed {exercise.name} with good form"
                db.session.add(workout_exercise)
            
            db.session.commit()
    
    return all_workouts

def create_progress_logs(users):
    """Create progress logs for users"""
    print("Creating progress logs...")
    
    for user in users:
        start_weight = user.weight
        target_weight = user.target_weight
        
        for week in range(8):
            log_date = datetime.now().date() - timedelta(weeks=(7 - week))
            
            # Simulate weight progression towards target
            progress_factor = week / 7
            current_weight = start_weight + (target_weight - start_weight) * progress_factor + random.uniform(-1, 1)
            
            progress_log = ProgressLog(
                user_id=user.id,
                log_date=log_date,
                weight=round(current_weight, 1),
                chest=round(random.uniform(90.0, 110.0), 1),
                waist=round(random.uniform(70.0, 90.0), 1),
                hips=round(random.uniform(95.0, 115.0), 1),
                biceps=round(random.uniform(30.0, 40.0), 1),
                thighs=round(random.uniform(55.0, 65.0), 1),
                notes=f"Week {week + 1}: Making steady progress toward my goal!"
            )
            
            db.session.add(progress_log)
        
        db.session.commit()

def main():
    with app.app_context():
        clear_database()
        
        users = create_users()
        exercises = create_exercises()
        workouts = create_workouts_and_exercises(users, exercises)
        create_progress_logs(users)
        
        print("Database seeded successfully!")
        print(f"Created {len(users)} users")
        print(f"Created {len(exercises)} exercises")
        print(f"Created {len(workouts)} workouts")
        print(f"Created {ProgressLog.query.count()} progress logs")
        print(f"Created {WorkoutExercise.query.count()} workout-exercise associations")

if __name__ == '__main__':
    main()