from flask import request, jsonify
from flask_restful import Resource
from models import db, WorkoutExercise
from routes.users import token_required

# -------------------------
# WorkoutExercises list (GET all, POST new)
# -------------------------
class WorkoutExerciseListResource(Resource):
    @token_required
    def get(current_user, self):
        entries = WorkoutExercise.query.all()
        return jsonify([e.to_dict() for e in entries])

    @token_required
    def post(current_user, self):
        data = request.get_json()
        try:
            entry = WorkoutExercise(
                user_id=current_user.id,
                workout_id=data['workout_id'],
                exercise_id=data['exercise_id'],
                sets=data.get('sets'),
                reps=data.get('reps'),
                weight=data.get('weight'),
                duration=data.get('duration'),
                distance=data.get('distance'),
                calories_burned=data.get('calories_burned'),
                order=data.get('order'),
                notes=data.get('notes')
            )
            db.session.add(entry)
            db.session.commit()
            return jsonify({'message': 'WorkoutExercise created', 'entry': entry.to_dict()}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

# -------------------------
# Single WorkoutExercise (GET, PUT, DELETE)
# -------------------------
class WorkoutExerciseResource(Resource):
    @token_required
    def get(current_user, self, we_id):
        entry = WorkoutExercise.query.get(we_id)
        if not entry:
            return jsonify({'error': 'WorkoutExercise not found'}), 404
        return jsonify(entry.to_dict())

    @token_required
    def put(current_user, self, we_id):
        entry = WorkoutExercise.query.get(we_id)
        if not entry:
            return jsonify({'error': 'WorkoutExercise not found'}), 404
        data = request.get_json()
        try:
            for key, value in data.items():
                if hasattr(entry, key):
                    setattr(entry, key, value)
            db.session.commit()
            return jsonify({'message': 'WorkoutExercise updated', 'entry': entry.to_dict()})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    @token_required
    def delete(current_user, self, we_id):
        entry = WorkoutExercise.query.get(we_id)
        if not entry:
            return jsonify({'error': 'WorkoutExercise not found'}), 404
        db.session.delete(entry)
        db.session.commit()
        return jsonify({'message': 'WorkoutExercise deleted'}), 200
