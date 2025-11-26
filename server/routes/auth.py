from flask_restful import Resource
from flask import request, jsonify
from models import User, db
from utils.jwt_handler import create_token

class RegisterAPI(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not all([username, email, password]):
            return {"error": "Missing required fields"}, 400
        if User.query.filter_by(username=username).first():
            return {"error": "Username already exists"}, 400
        if User.query.filter_by(email=email).first():
            return {"error": "Email already exists"}, 400

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return {"message": "User registered successfully", "user": user.to_dict()}, 201

class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not all([username, password]):
            return {"error": "Missing username or password"}, 400

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return {"error": "Invalid credentials"}, 401

        token = create_token(user.id)
        if not token:
            return{"error":"Token creation failed"}, 500
        
        return jsonify({"message": "Login successful", "token": token, "user": user.to_dict()})
