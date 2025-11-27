from flask_restful import Resource
from flask import request, jsonify
from models import db, WorkoutExercise
from utils.jwt_handler import token_required

class WorkoutExerciseResource(Resource):
    @token_required
    def get(self, current_user, we_id):
        entry = WorkoutExercise.query.get(we_id)
        if not entry:
            return {"error": "WorkoutExercise not found"}, 404
        return entry.to_dict(), 200

    @token_required
    def put(self, current_user, we_id):
        entry = WorkoutExercise.query.get(we_id)
        if not entry:
            return {"error": "WorkoutExercise not found"}, 404
        data = request.get_json()
        for key, value in data.items():
            if hasattr(entry, key):
                setattr(entry, key, value)
        db.session.commit()
        return {"message": "WorkoutExercise updated", "entry": entry.to_dict()}, 200

    @token_required
    def delete(self, current_user, we_id):
        entry = WorkoutExercise.query.get(we_id)
        if not entry:
            return {"error": "WorkoutExercise not found"}, 404
        db.session.delete(entry)
        db.session.commit()
        return {"message": "WorkoutExercise deleted"}, 200

class WorkoutExerciseListResource(Resource):
    @token_required
    def get(self, current_user):
        return [e.to_dict() for e in WorkoutExercise.query.all()], 200

    @token_required
    def post(self, current_user):
        data = request.get_json()
        entry = WorkoutExercise(
            user_id=current_user.id,
            workout_id=data['workout_id'],
            exercise_id=data['exercise_id'],
            sets=data.get('sets'),
            reps=data.get('reps'),
            weight=data.get('weight'),
            duration=data.get('duration'),
            distance=data.get('distance'),
            notes=data.get('notes'),
            order=data.get('order')
        )
        db.session.add(entry)
        db.session.commit()
        return {"message": "WorkoutExercise created", "entry": entry.to_dict()}, 201
