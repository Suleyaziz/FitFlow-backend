from flask import request
from flask_restful import Resource
from models import db, Workout
from utils.jwt_handler import token_required

class WorkoutResource(Resource):
    @token_required
    def get(self, current_user, workout_id=None):  # ← FIXED: self first!
        if workout_id:
            workout = Workout.query.get(workout_id)
            if not workout:
                return {"error": "Workout not found"}, 404
            return workout.to_dict(), 200
        workouts = Workout.query.all()
        return [w.to_dict() for w in workouts], 200

    @token_required
    def post(self, current_user):  # ← FIXED: self first!
        data = request.get_json()
        try:
            workout = Workout(
                user_id=current_user.id,
                name=data['name'],
                description=data.get('description'),
                duration=data.get('duration'),
                calories_burned=data.get('calories_burned'),
                workout_type=data.get('workout_type')
            )
            db.session.add(workout)
            db.session.commit()
            return {"message": "Workout created", "workout": workout.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400

    @token_required
    def put(self, current_user, workout_id):  # ← FIXED: self first!
        workout = Workout.query.get(workout_id)
        if not workout:
            return {"error": "Workout not found"}, 404
        data = request.get_json()
        for key in ['name', 'description', 'duration', 'calories_burned', 'workout_type']:
            if key in data:
                setattr(workout, key, data[key])
        db.session.commit()
        return {"message": "Workout updated", "workout": workout.to_dict()}, 200

    @token_required
    def delete(self, current_user, workout_id):  # ← FIXED: self first!
        workout = Workout.query.get(workout_id)
        if not workout:
            return {"error": "Workout not found"}, 404
        db.session.delete(workout)
        db.session.commit()
        return {"message": "Workout deleted"}, 200