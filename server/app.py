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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
app.secret_key = os.environ.get('SECRET_KEY') or 'fitflow-secret-key-2024'

# Database setup
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)

# Initialize extensions (models will be imported later)
migrate = Migrate(app, db)
db.init_app(app)

# Create API and enable CORS
api = Api(app)
CORS(app)

# Import models AFTER db is created to avoid circular imports
# This import happens after all the setup is complete

@app.route('/')
def index():
    return '<h1>FitFlow Fitness Tracker API</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)