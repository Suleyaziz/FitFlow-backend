from flask import request
from flask_restful import Resource
from server.models import Exercise
from server.extensions import db

class ExerciseResource(Resource):
    def get(self, exercise_id=None):
        if exercise_id:
            exercise = Exercise.query.get(exercise_id)
            if not exercise:
                return {"message": "Exercise not found"}, 404
            return exercise.to_dict(), 200
        exercises = Exercise.query.all()
        return [e.to_dict() for e in exercises], 200

    def post(self):
        data = request.get_json()
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
        return {"message": "Exercise created", "exercise": exercise.to_dict()}, 201

    def put(self, exercise_id):
        exercise = Exercise.query.get(exercise_id)
        if not exercise:
            return {"message": "Exercise not found"}, 404
        data = request.get_json()
        for key in ["name", "category", "muscle_group", "description"]:
            if key in data:
                setattr(exercise, key, data[key])
        db.session.commit()
        return {"message": "Exercise updated", "exercise": exercise.to_dict()}, 200

    def delete(self, exercise_id):
        exercise = Exercise.query.get(exercise_id)
        if not exercise:
            return {"message": "Exercise not found"}, 404
        db.session.delete(exercise)
        db.session.commit()
        return {"message": "Exercise deleted"}, 200
