"""
Authentication endpoints: register and login.

- POST /api/register  -> create account (username, email, password)
- POST /api/login     -> login using email (or username) + password -> returns JWT
"""

from flask import Blueprint, request, jsonify
from server.models import db, User
from server.utils.jwt_handler import create_token
from server.extensions import db


auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # basic validation
    if not username or not email or not password:
        return jsonify({"error": "username, email and password required"}), 400

    # check uniqueness
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "username or email already exists"}), 409

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "invalid credentials"}), 401

    token = create_token(user.id)
    return jsonify({"token": token, "user": user.to_dict()}), 200
