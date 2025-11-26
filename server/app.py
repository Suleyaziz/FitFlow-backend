import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

# Import db from models (your work)
from models import db

# Create Flask app
app = Flask(__name__)

# Database configuration (your work)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
app.secret_key = os.environ.get('SECRET_KEY') or 'fitflow-secret-key-2024'

# Initialize database extensions (your work)
migrate = Migrate(app, db)
db.init_app(app)

# Create API and enable CORS
api = Api(app)
CORS(app)

@app.route('/')
def index():
    return '<h1>FitFlow Fitness Tracker API</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)