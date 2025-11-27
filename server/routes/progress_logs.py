from flask import request
from flask_restful import Resource
from models import db, ProgressLog
from server.utils.jwt_handler import token_required

class ProgressLogResource(Resource):
    @token_required
    def get(self, current_user, log_id=None):
        if log_id:
            # FIXED: Filter by user_id
            log = ProgressLog.query.filter_by(
                id=log_id,
                user_id=current_user.id
            ).first()
            if not log:
                return {"error": "Progress log not found"}, 404
            return log.to_dict(), 200
        
        # Already filtered by user - good!
        logs = ProgressLog.query.filter_by(user_id=current_user.id).all()
        return [l.to_dict() for l in logs], 200

    @token_required
    def post(self, current_user):  # Fixed: self first
        data = request.get_json()
        try:
            log = ProgressLog(
                user_id=current_user.id,
                log_date=data.get('log_date'),
                weight=data.get('weight'),
                chest=data.get('chest'),
                waist=data.get('waist'),
                hips=data.get('hips'),
                biceps=data.get('biceps'),
                thighs=data.get('thighs'),
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
        # FIXED: Verify user owns this log
        log = ProgressLog.query.filter_by(
            id=log_id,
            user_id=current_user.id
        ).first()
        if not log:
            return {"error": "Progress log not found"}, 404
        
        data = request.get_json()
        for key in ['log_date', 'weight', 'chest', 'waist', 'hips', 'biceps', 'thighs', 'notes']:
            if key in data:
                setattr(log, key, data[key])
        db.session.commit()
        return {"message": "Progress log updated", "log": log.to_dict()}, 200

    @token_required
    def delete(self, current_user, log_id):
        # FIXED: Verify user owns this log
        log = ProgressLog.query.filter_by(
            id=log_id,
            user_id=current_user.id
        ).first()
        if not log:
            return {"error": "Progress log not found"}, 404
        db.session.delete(log)
        db.session.commit()
        return {"message": "Progress log deleted"}, 200