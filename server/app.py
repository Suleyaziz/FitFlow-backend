import os
from flask import Flask, request, jsonify
from functools import wraps
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

# Import db from models instead of creating a new one
from models import db

# Create Flask app
app = Flask(__name__)

# App configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
app.secret_key = os.environ.get('SECRET_KEY') or 'fitflow-secret-key-2024'

# Initialize extensions with the db from models
migrate = Migrate(app, db)
db.init_app(app)

# Create API and enable CORS
api = Api(app)
CORS(app)

# Import models AFTER db is initialized
from models import User

@app.route('/')
def index():
    return '<h1>FitFlow Fitness Tracker API</h1>'

# Auth routes
@app.route('/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            age=data.get('age'),
            height=data.get('height'),
            weight=data.get('weight'),
            fitness_goal=data.get('fitness_goal'),
            target_weight=data.get('target_weight')
        )
        
        # Set password
        user.set_password(data['password'])
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        # Generate token
        token = user.generate_token()
        
        return jsonify({
            'token': token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == data['username']) | (User.email == data['username'])
        ).first()
        
        # Check user exists and password is correct
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Generate token
        token = user.generate_token()
        
        return jsonify({
            'token': token,
            'user': user.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/auth/me', methods=['GET'])
def get_current_user():
    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token required'}), 401
        
        token = auth_header.split(' ')[1]
        
        user = User.verify_token(token)
        
        if not user:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        return jsonify({'user': user.to_dict()})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Authentication middleware
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'error': 'Token required'}), 401
            
            token = auth_header.split(' ')[1]
            
            user = User.verify_token(token)
            
            if not user:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            # Add user to request context for use in routes
            request.current_user = user
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)}), 401
    return decorated

# Example protected route
@app.route('/protected', methods=['GET'])
@token_required
def protected_route():
    return jsonify({'message': f'Hello {request.current_user.username}! This is protected.'})

if __name__ == '__main__':
    app.run(port=5555, debug=True)