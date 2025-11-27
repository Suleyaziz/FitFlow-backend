import jwt
from functools import wraps
from flask import request, jsonify, current_app
from models import User


def create_token(user_id):
    payload = {"user_id": user_id}
    token = jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", None)
        if not token:
            return jsonify({"error": "Token missing"}), 401
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        try:
            data = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
            user_id = data.get("user_id")
            user = User.query.get(user_id)
            if not user:
                raise Exception("User not found")
        except Exception:
            return jsonify({"error": "Invalid or expired token"}), 401
        return f(current_user=user, *args, **kwargs)
    return decorated
