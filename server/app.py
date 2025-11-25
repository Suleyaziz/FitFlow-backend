# server/app.py
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from server.config import Config
from server.extensions import db, migrate
from server.routes import register_routes

def create_app():
    """Flask application factory with error handling"""
    try:
        app = Flask(__name__)
        app.config.from_object(Config)

        # Enable CORS
        CORS(app)

        # Initialize DB and migrations
        db.init_app(app)
        migrate.init_app(app, db)

        # RESTful API
        api = Api(app)
        register_routes(api)  # function to register all resource routes

        # Health check / root endpoint
        @app.route('/')
        def index():
            return jsonify({"message": "FitFlow Fitness Tracker API is running"}), 200

        # Global error handler for unhandled exceptions
        @app.errorhandler(Exception)
        def handle_exception(e):
            # Return JSON instead of HTML for errors
            response = {
                "error": str(e),
                "message": "An unexpected error occurred"
            }
            return jsonify(response), 500

        return app

    except Exception as e:
        # If the app fails to load, print the error and exit
        print(f"Failed to create app: {e}")
        raise

# Allows running directly with `python server/app.py`
if __name__ == "__main__":
    try:
        app = create_app()
        app.run(port=5555, debug=True)
    except Exception as e:
        print(f"Failed to start Flask server: {e}")
