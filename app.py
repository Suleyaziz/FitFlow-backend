from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from config import Config
from extensions import db, migrate  # ← Now in same directory
from server.routes import register_routes  # ← Changed

def create_app():
    """Flask application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # IMPROVED CORS - allows all origins for development
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    })

    db.init_app(app)
    migrate.init_app(app, db)

    # FIXED: Create tables if they don't exist (since migrations folder is missing)
    with app.app_context():
        db.create_all()

    api = Api(app)  
    register_routes(api)

    @app.route('/')
    def index():
        return jsonify({"message": "FitFlow Fitness Tracker API is running"}), 200

    @app.route('/api/health')
    def health():
        return jsonify({"status": "healthy"}), 200

    @app.errorhandler(Exception)
    def handle_exception(e):
        import traceback
        print(f"❌ ERROR: {str(e)}")
        traceback.print_exc()
        
        response = jsonify({
            "error": str(e), 
            "message": "An unexpected error occurred"
        })
        response.status_code = 500
        
        # ⚠️ CRITICAL: Add CORS headers to error responses
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        
        return response

    # Handle CORS preflight requests
    @app.after_request
    def after_request(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
        return response

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5555, debug=True)