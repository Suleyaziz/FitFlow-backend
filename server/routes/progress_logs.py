from flask import request, jsonify
from flask_restful import Resource
from models import db, ProgressLog
from utils.jwt_handler import token_required
from datetime import datetime



class ProgressLogResource(Resource):
    @token_required
    def get(self, current_user, log_id=None):
        if log_id:
            log = ProgressLog.query.get(log_id)
            if not log:
                return {"error": "Progress log not found"}, 404
            # Check ownership
            if log.user_id != current_user.id:
                return {"error": "Unauthorized access to this progress log"}, 403
            return log.to_dict(), 200
        logs = ProgressLog.query.filter_by(user_id=current_user.id).all()
        return [l.to_dict() for l in logs], 200

    @token_required
    def post(self, current_user):
        data = request.get_json()
        try:
            # Extract measurements from nested object if provided
            measurements = data.get('measurements', {})
            
            log_date_str = data.get('date') or data.get('log_date')
            try:
                log_date = datetime.strptime(log_date_str, '%Y-%m-%d').date() if log_date_str else datetime.utcnow().date()
            except ValueError:
                return {"error": "Invalid date format. Use YYYY-MM-DD"}, 400

            log = ProgressLog(
                user_id=current_user.id,
                log_date=log_date,
                weight=data.get('weight'),
                body_fat=data.get('bodyFat'),
                chest=measurements.get('chest'),
                waist=measurements.get('waist'),
                hips=measurements.get('hips'),
                biceps=measurements.get('arms'),  # Map arms to biceps
                thighs=measurements.get('thighs'),
                notes=data.get('notes')
            )
            db.session.add(log)
            db.session.commit()
            return {"message": "Progress log created", "log": log.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400

    @token_required
    def put(self, current_user, log_id):
        log = ProgressLog.query.get(log_id)
        if not log:
            return {"error": "Progress log not found"}, 404
        # Check ownership
        if log.user_id != current_user.id:
            return {"error": "Unauthorized access to this progress log"}, 403
        data = request.get_json()
        
        # Handle measurements object if provided
        measurements = data.get('measurements', {})
        
        # Update simple fields
        if 'date' in data or 'log_date' in data:
            log_date_str = data.get('date') or data.get('log_date')
            try:
                log.log_date = datetime.strptime(log_date_str, '%Y-%m-%d').date() if log_date_str else log.log_date
            except ValueError:
                return {"error": "Invalid date format. Use YYYY-MM-DD"}, 400
        if 'weight' in data:
            log.weight = data.get('weight')
        if 'bodyFat' in data:
            log.body_fat = data.get('bodyFat')
        if 'notes' in data:
            log.notes = data.get('notes')
            
        # Update measurements
        if measurements:
            if 'chest' in measurements:
                log.chest = measurements.get('chest')
            if 'waist' in measurements:
                log.waist = measurements.get('waist')
            if 'hips' in measurements:
                log.hips = measurements.get('hips')
            if 'arms' in measurements:
                log.biceps = measurements.get('arms')
            if 'thighs' in measurements:
                log.thighs = measurements.get('thighs')
        
        db.session.commit()
        return {"message": "Progress log updated", "log": log.to_dict()}, 200

    @token_required
    def delete(self, current_user, log_id):
        log = ProgressLog.query.get(log_id)
        if not log:
            return {"error": "Progress log not found"}, 404
        # Check ownership
        if log.user_id != current_user.id:
            return {"error": "Unauthorized access to this progress log"}, 403
        db.session.delete(log)
        db.session.commit()
        return {"message": "Progress log deleted"}, 200
