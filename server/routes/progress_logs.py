from flask import request
from flask_restful import Resource
from server.models import ProgressLog
from server.extensions import db

class ProgressLogResource(Resource):
    def get(self, log_id=None):
        if log_id:
            log = ProgressLog.query.get(log_id)
            if not log:
                return {"message": "Progress log not found"}, 404
            return log.to_dict(), 200
        logs = ProgressLog.query.all()
        return [l.to_dict() for l in logs], 200

    def post(self):
        data = request.get_json()
        log = ProgressLog(**data)
        db.session.add(log)
        db.session.commit()
        return {"message": "Progress log created", "progress_log": log.to_dict()}, 201

    def put(self, log_id):
        log = ProgressLog.query.get(log_id)
        if not log:
            return {"message": "Progress log not found"}, 404
        data = request.get_json()
        for key in ["weight","chest","waist","hips","biceps","thighs","notes"]:
            if key in data:
                setattr(log, key, data[key])
        db.session.commit()
        return {"message": "Progress log updated", "progress_log": log.to_dict()}, 200

    def delete(self, log_id):
        log = ProgressLog.query.get(log_id)
        if not log:
            return {"message": "Progress log not found"}, 404
        db.session.delete(log)
        db.session.commit()
        return {"message": "Progress log deleted"}, 200
