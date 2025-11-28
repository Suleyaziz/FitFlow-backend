from flask import request
from flask_restful import Resource
from models import db, Workout
from server.utils.jwt_handler import token_required

class WorkoutResource(Resource):
    @token_required
    def get(self, current_user, workout_id=None):
        if workout_id:
            # FIXED: Filter by user_id to prevent accessing other users' workouts
            workout = Workout.query.filter_by(
                id=workout_id,
                user_id=current_user.id
            ).first()
            if not workout:
                return {"error": "Workout not found"}, 404
            return workout.to_dict(), 200
        
        # FIXED: Only return current user's workouts
        workouts = Workout.query.filter_by(user_id=current_user.id).all()
        return [w.to_dict() for w in workouts], 200

    @token_required
    def post(self, current_user):  # ← FIXED: self first!
        data = request.get_json()
        try:
            # Parse date string to date object
            from datetime import datetime
            workout_date = data.get('date')
            if workout_date and isinstance(workout_date, str):
                workout_date = datetime.strptime(workout_date, '%Y-%m-%d').date()
            
            workout = Workout(
                user_id=current_user.id,
                name=data['name'],
                description=data.get('description'),
                date=workout_date,
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
    def put(self, current_user, workout_id):
        # FIXED: Verify user owns this workout
        workout = Workout.query.filter_by(
            id=workout_id,
            user_id=current_user.id
        ).first()
        if not workout:
            return {"error": "Workout not found"}, 404
        
        data = request.get_json()
        
        # Parse date if provided
        from datetime import datetime
        if 'date' in data and isinstance(data['date'], str):
            data['date'] = datetime.strptime(data['date'], '%Y-%m-%d').date()
        
        for key in ['name', 'description', 'date', 'duration', 'calories_burned', 'workout_type']:
            if key in data:
                setattr(workout, key, data[key])
        db.session.commit()
        return {"message": "Workout updated", "workout": workout.to_dict()}, 200

    @token_required
    def delete(self, current_user, workout_id):
        # FIXED: Verify user owns this workout
        workout = Workout.query.filter_by(
            id=workout_id,
            user_id=current_user.id
        ).first()
        if not workout:
            return {"error": "Workout not found"}, 404
        db.session.delete(workout)
        db.session.commit()
        return {"message": "Workout deleted"}, 200