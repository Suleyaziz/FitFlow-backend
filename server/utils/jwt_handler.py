from functools import wraps
from flask import request, jsonify, current_app
import jwt
from server.models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        try:
            payload = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
            current_user = User.query.get(payload["user_id"])
            if not current_user:
                return jsonify({"message": "User not found"}), 404
        except Exception as e:
            return jsonify({"message": "Token is invalid", "error": str(e)}), 401
        return f(current_user, *args, **kwargs)
    return decorated
