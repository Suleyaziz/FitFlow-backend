"""
Exercise CRUD routes - protected.
Exercises are global library items (unique by name). Creation is protected (only logged-in).
"""

from flask import Blueprint, request, jsonify
from server.models import db, Exercise
from server.utils.jwt_handler import token_required
from server.extensions import db


exercise_bp = Blueprint("exercise_bp", __name__)

@exercise_bp.route("/exercises", methods=["GET"])
@token_required
def list_exercises():
    exercises = Exercise.query.all()
    return jsonify([e.to_dict() for e in exercises]), 200

@exercise_bp.route("/exercises/<int:exercise_id>", methods=["GET"])
@token_required
def get_exercise(exercise_id):
    ex = Exercise.query.get(exercise_id)
    if not ex:
        return jsonify({"error": "Exercise not found"}), 404
    return jsonify(ex.to_dict()), 200

@exercise_bp.route("/exercises", methods=["POST"])
@token_required
def create_exercise():
    data = request.get_json() or {}
    name = data.get("name")
    category = data.get("category")
    if not name or not category:
        return jsonify({"error": "name and category required"}), 400
    ex = Exercise(name=name, category=category, muscle_group=data.get("muscle_group"), description=data.get("description"))
    db.session.add(ex)
    db.session.commit()
    return jsonify(ex.to_dict()), 201

@exercise_bp.route("/exercises/<int:exercise_id>", methods=["PATCH"])
@token_required
def update_exercise(exercise_id):
    ex = Exercise.query.get(exercise_id)
    if not ex:
        return jsonify({"error": "Exercise not found"}), 404
    data = request.get_json() or {}
    for k in ("name","category","muscle_group","description"):
        if k in data:
            setattr(ex,k,data[k])
    db.session.commit()
    return jsonify(ex.to_dict()), 200

@exercise_bp.route("/exercises/<int:exercise_id>", methods=["DELETE"])
@token_required
def delete_exercise(exercise_id):
    ex = Exercise.query.get(exercise_id)
    if not ex:
        return jsonify({"error": "Exercise not found"}), 404
    db.session.delete(ex)
    db.session.commit()
    return "", 204
