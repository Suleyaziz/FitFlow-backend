from flask import request, jsonify
from flask_restful import Resource
from models import db, Exercise
from utils.jwt_handler import token_required

class ExerciseResource(Resource):
    @token_required
    def get(current_user, self, exercise_id=None):
        if exercise_id:
            exercise = Exercise.query.get(exercise_id)
            if not exercise:
                return {"error": "Exercise not found"}, 404
            return exercise.to_dict(), 200
        exercises = Exercise.query.all()
        return [e.to_dict() for e in exercises], 200

    @token_required
    def post(current_user, self):
        data = request.get_json()
        try:
            exercise = Exercise(
                name=data['name'],
                category=data['category'],
                muscle_group=data.get('muscle_group'),
                description=data.get('description')
            )
            db.session.add(exercise)
            db.session.commit()
            return {"message": "Exercise created", "exercise": exercise.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400

    @token_required
    def put(current_user, self, exercise_id):
        exercise = Exercise.query.get(exercise_id)
        if not exercise:
            return {"error": "Exercise not found"}, 404
        data = request.get_json()
        for key in ['name', 'category', 'muscle_group', 'description']:
            if key in data:
                setattr(exercise, key, data[key])
        db.session.commit()
        return {"message": "Exercise updated", "exercise": exercise.to_dict()}, 200

    @token_required
    def delete(current_user, self, exercise_id):
        exercise = Exercise.query.get(exercise_id)
        if not exercise:
            return {"error": "Exercise not found"}, 404
        db.session.delete(exercise)
        db.session.commit()
        return {"message": "Exercise deleted"}, 200
