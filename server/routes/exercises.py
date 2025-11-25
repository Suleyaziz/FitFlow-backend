from flask import request
from flask_restful import Resource
from server.models import WorkoutExercise
from server.extensions import db

class WorkoutExerciseResource(Resource):
    def get(self, we_id=None):
        if we_id:
            we = WorkoutExercise.query.get(we_id)
            if not we:
                return {"message": "WorkoutExercise not found"}, 404
            return we.to_dict(), 200
        all_we = WorkoutExercise.query.all()
        return [w.to_dict() for w in all_we], 200

    def post(self):
        data = request.get_json()
        we = WorkoutExercise(**data)
        db.session.add(we)
        db.session.commit()
        return {"message": "WorkoutExercise created", "workout_exercise": we.to_dict()}, 201

    def put(self, we_id):
        we = WorkoutExercise.query.get(we_id)
        if not we:
            return {"message": "WorkoutExercise not found"}, 404
        data = request.get_json()
        for key in ["sets","reps","weight","duration","distance","notes","order"]:
            if key in data:
                setattr(we, key, data[key])
        db.session.commit()
        return {"message": "WorkoutExercise updated", "workout_exercise": we.to_dict()}, 200

    def delete(self, we_id):
        we = WorkoutExercise.query.get(we_id)
        if not we:
            return {"message": "WorkoutExercise not found"}, 404
        db.session.delete(we)
        db.session.commit()
        return {"message": "WorkoutExercise deleted"}, 200
