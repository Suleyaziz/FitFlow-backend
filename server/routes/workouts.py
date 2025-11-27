from flask import request, jsonify
from flask_restful import Resource
from models import db, Workout, Exercise, WorkoutExercise
from datetime import datetime


from utils.jwt_handler import token_required


class WorkoutResource(Resource):
    @token_required
    def get(self, current_user, workout_id=None):
        if workout_id:
            workout = Workout.query.get(workout_id)
            if not workout:
                return {"error": "Workout not found"}, 404
            # Check ownership
            if workout.user_id != current_user.id:
                return {"error": "Unauthorized access to this workout"}, 403
            return workout.to_dict(), 200
        # Filter workouts by current user
        workouts = Workout.query.filter_by(user_id=current_user.id).all()
        return [w.to_dict() for w in workouts], 200

    @token_required
    def post(self, current_user):
        data = request.get_json()
        try:
            date_str = data.get('date')
            try:
                workout_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.utcnow().date()
            except ValueError:
                return {"error": "Invalid date format. Use YYYY-MM-DD"}, 400

            workout = Workout(
                user_id=current_user.id,
                name=data['name'],
                description=data.get('description'),
                date=workout_date,
                duration=data.get('duration'),
                calories=data.get('calories'),
                workout_type=data.get('workout_type')
            )
            db.session.add(workout)
            db.session.flush()  # Flush to get workout ID

            # Handle exercises
            exercises_data = data.get('exercises', [])
            for ex_data in exercises_data:
                # Find or create exercise
                exercise_name = ex_data.get('name')
                if not exercise_name:
                    continue
                    
                exercise = Exercise.query.filter_by(name=exercise_name).first()
                if not exercise:
                    # Create new exercise if it doesn't exist (basic info)
                    exercise = Exercise(name=exercise_name, category="Strength", description="Custom exercise")
                    db.session.add(exercise)
                    db.session.flush()
                
                # Create workout exercise link
                workout_exercise = WorkoutExercise(
                    user_id=current_user.id,
                    workout_id=workout.id,
                    exercise_id=exercise.id,
                    sets=ex_data.get('sets'),
                    reps=ex_data.get('reps'),
                    weight=ex_data.get('weight'),
                    duration=ex_data.get('duration'),
                    distance=ex_data.get('distance')
                )
                db.session.add(workout_exercise)

            db.session.commit()
            return {"message": "Workout created", "workout": workout.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


    @token_required
    def put(self, current_user, workout_id):
        workout = Workout.query.get(workout_id)
        if not workout:
            return {"error": "Workout not found"}, 404
        # Check ownership
        if workout.user_id != current_user.id:
            return {"error": "Unauthorized access to this workout"}, 403
        data = request.get_json()
        for key in ['name', 'description', 'duration', 'calories', 'workout_type']:
            if key in data:
                setattr(workout, key, data[key])
        db.session.commit()
        return {"message": "Workout updated", "workout": workout.to_dict()}, 200

    @token_required
    def delete(self, current_user, workout_id):
        workout = Workout.query.get(workout_id)
        if not workout:
            return {"error": "Workout not found"}, 404
        # Check ownership
        if workout.user_id != current_user.id:
            return {"error": "Unauthorized access to this workout"}, 403
        db.session.delete(workout)
        db.session.commit()
        return {"message": "Workout deleted"}, 200
