from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
import re
from datetime import datetime, timedelta
import hashlib
import secrets
import jwt
import os

# Create db instance here
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Fitness profile
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    fitness_goal = db.Column(db.String(200))
    target_weight = db.Column(db.Float)
    experience_level = db.Column(db.String(20), default='Beginner')
    daily_calorie_goal = db.Column(db.Integer)
    
    # Relationships
    workouts = db.relationship('Workout', backref='user', cascade='all, delete-orphan', lazy=True)
    progress_logs = db.relationship('ProgressLog', backref='user', cascade='all, delete-orphan', lazy=True)
    workout_exercises = db.relationship('WorkoutExercise', backref='user', cascade='all, delete-orphan', lazy=True)
    
    serialize_rules = ('-password_hash', '-workouts.user', '-progress_logs.user', '-workout_exercises.user')
    
    @validates('username')
    def validate_username(self, key, username):
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return username
    
    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("Invalid email format")
        return email
    
    @validates('age')
    def validate_age(self, key, age):
        if age is not None and (age < 13 or age > 120):
            raise ValueError("Age must be between 13 and 120")
        return age
    
    def set_password(self, password):
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        self.password_hash = f"{salt}${password_hash}"
    
    def check_password(self, password):
        if not self.password_hash or '$' not in self.password_hash:
            return False
        salt, stored_hash = self.password_hash.split('$')
        test_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return test_hash == stored_hash
    
    def generate_token(self, expires_in=3600):
        payload = {
            'user_id': self.id,
            'username': self.username,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in)
        }
        secret_key = os.environ.get('JWT_SECRET_KEY') or 'fitflow-jwt-secret-key-2024'
        return jwt.encode(payload, secret_key, algorithm='HS256')
    
    @staticmethod
    def verify_token(token):
        try:
            secret_key = os.environ.get('JWT_SECRET_KEY') or 'fitflow-jwt-secret-key-2024'
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return User.query.get(payload['user_id'])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

class Workout(db.Model, SerializerMixin):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer)
    calories_burned = db.Column(db.Float)
    workout_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    workout_exercises = db.relationship('WorkoutExercise', backref='workout', cascade='all, delete-orphan', lazy=True)
    exercises = association_proxy('workout_exercises', 'exercise')
    
    serialize_rules = ('-user.workouts', '-user.progress_logs', '-user.workout_exercises', 
                      '-workout_exercises.workout', '-workout_exercises.user')

class Exercise(db.Model, SerializerMixin):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    muscle_group = db.Column(db.String(50))
    equipment = db.Column(db.String(50))
    difficulty = db.Column(db.String(20), default='Intermediate')
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    calories_per_minute = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    workout_exercises = db.relationship('WorkoutExercise', backref='exercise', cascade='all, delete-orphan', lazy=True)
    workouts = association_proxy('workout_exercises', 'workout')
    
    serialize_rules = ('-workout_exercises.exercise',)

class WorkoutExercise(db.Model, SerializerMixin):
    __tablename__ = 'workout_exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight = db.Column(db.Float)
    duration = db.Column(db.Integer)
    distance = db.Column(db.Float)
    calories_burned = db.Column(db.Float)
    order = db.Column(db.Integer)
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    serialize_rules = ('-user.workouts', '-user.progress_logs', '-user.workout_exercises',
                      '-workout.workout_exercises', '-exercise.workout_exercises')

class ProgressLog(db.Model, SerializerMixin):
    __tablename__ = 'progress_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    log_date = db.Column(db.Date, nullable=False)
    
    weight = db.Column(db.Float)
    chest = db.Column(db.Float)
    waist = db.Column(db.Float)
    hips = db.Column(db.Float)
    biceps = db.Column(db.Float)
    thighs = db.Column(db.Float)
    body_fat_percentage = db.Column(db.Float)
    mood = db.Column(db.String(20))
    energy_level = db.Column(db.Integer)
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    serialize_rules = ('-user.workouts', '-user.progress_logs', '-user.workout_exercises')