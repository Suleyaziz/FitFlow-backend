from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from config import Config
from extensions import db, migrate
from routes import register_routes

def create_app():
    """Flask application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)
    register_routes(api)

    @app.route('/')
    def index():
        return jsonify({"message": "FitFlow Fitness Tracker API is running"}), 200

    @app.errorhandler(Exception)
    def handle_exception(e):
        response = {"error": str(e), "message": "An unexpected error occurred"}
        return jsonify(response), 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5555, debug=True)
