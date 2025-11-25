from flask import request
from flask_restful import Resource
from server.models import Workout
from server.extensions import db

class WorkoutResource(Resource):
    def get(self, workout_id=None):
        if workout_id:
            workout = Workout.query.get(workout_id)
            if not workout:
                return {"message": "Workout not found"}, 404
            return workout.to_dict(), 200
        workouts = Workout.query.all()
        return [w.to_dict() for w in workouts], 200

    def post(self):
        data = request.get_json()
        workout = Workout(**data)
        db.session.add(workout)
        db.session.commit()
        return {"message": "Workout created", "workout": workout.to_dict()}, 201

    def put(self, workout_id):
        workout = Workout.query.get(workout_id)
        if not workout:
            return {"message": "Workout not found"}, 404
        data = request.get_json()
        for key in ["name", "description", "date", "duration", "calories_burned", "workout_type"]:
            if key in data:
                setattr(workout, key, data[key])
        db.session.commit()
        return {"message": "Workout updated", "workout": workout.to_dict()}, 200

    def delete(self, workout_id):
        workout = Workout.query.get(workout_id)
        if not workout:
            return {"message": "Workout not found"}, 404
        db.session.delete(workout)
        db.session.commit()
        return {"message": "Workout deleted"}, 200
