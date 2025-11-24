import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Create Flask app
app = Flask(__name__)

# App configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Use SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
app.json.compact = False  # Pretty print JSON
app.secret_key = os.environ.get('SECRET_KEY') or 'fitflow-secret-key-2024'  # For sessions

# Database setup with naming conventions
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)  # Create database instance

# Import models after db is created
from models import User, Workout, Exercise, WorkoutExercise, ProgressLog

# Initialize database migration and connect to app
migrate = Migrate(app, db)
db.init_app(app)

# Create API and enable CORS
api = Api(app)  # REST API
CORS(app)  # Allow cross-origin requests

@app.route('/')
def index():
    return '<h1>FitFlow Fitness Tracker API</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)  # Run in debug mode on port 5555