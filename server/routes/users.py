# server/routes/users.py
from flask import request, jsonify, current_app
from flask_restful import Resource
from server.models import User
from server.extensions import db
import jwt
from datetime import datetime, timedelta

# In-memory token blacklist
BLACKLIST = set()

# User registration
class UserRegisterResource(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if User.query.filter_by(username=username).first():
            return {"message": "Username already exists"}, 400
        if User.query.filter_by(email=email).first():
            return {"message": "Email already exists"}, 400

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return {"message": "User registered successfully", "user": user.to_dict()}, 201

# User login
class UserLoginResource(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400

        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return {"message": "Invalid credentials"}, 401

        payload = {
            "user_id": user.id,
            "username": user.username,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")
        return {"message": "Login successful", "token": token}, 200

# User logout
class UserLogoutResource(Resource):
    def post(self):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return {"message": "Token missing"}, 400
        BLACKLIST.add(token)
        return {"message": "Logged out successfully"}, 200

# User profile CRUD
class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404
            return user.to_dict(), 200
        users = User.query.all()
        return [u.to_dict() for u in users], 200

    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        data = request.get_json()
        for key in ["username", "email", "age", "height", "weight", "fitness_goal", "target_weight"]:
            if key in data:
                setattr(user, key, data[key])
        if "password" in data:
            user.set_password(data["password"])
        db.session.commit()
        return {"message": "User updated", "user": user.to_dict()}, 200

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200
