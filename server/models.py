from app import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
import re
import hashlib
import secrets
from datetime import datetime

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Fitness profile fields
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    fitness_goal = db.Column(db.String(200))
    target_weight = db.Column(db.Float)
    
    # Relationships
    workouts = db.relationship('Workout', backref='user', cascade='all, delete-orphan')
    progress_logs = db.relationship('ProgressLog', backref='user', cascade='all, delete-orphan')
    workout_exercises = db.relationship('WorkoutExercise', backref='user', cascade='all, delete-orphan')
    
    # Serialization rules
    serialize_rules = ('-password_hash', '-workouts.user', '-progress_logs.user', '-workout_exercises.user')
    
    # Validations
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
        # Simple password hashing without bcrypt
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        self.password_hash = f"{salt}${password_hash}"
    
    def check_password(self, password):
        if not self.password_hash or '$' not in self.password_hash:
            return False
        salt, stored_hash = self.password_hash.split('$')
        test_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return test_hash == stored_hash

class Workout(db.Model, SerializerMixin):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer)
    calories_burned = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', backref='workout', cascade='all, delete-orphan')
    
    # Association proxy
    exercises = association_proxy('workout_exercises', 'exercise')
    
    # Serialization rules
    serialize_rules = ('-user.workouts', '-user.progress_logs', '-user.workout_exercises', 
                      '-workout_exercises.workout', '-workout_exercises.user')
    
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 2:
            raise ValueError("Workout name must be at least 2 characters long")
        return name
    
    @validates('duration')
    def validate_duration(self, key, duration):
        if duration is not None and duration < 1:
            raise ValueError("Duration must be at least 1 minute")
        return duration

class Exercise(db.Model, SerializerMixin):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    muscle_group = db.Column(db.String(50))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', backref='exercise', cascade='all, delete-orphan')
    
    # Association proxy
    workouts = association_proxy('workout_exercises', 'workout')
    
    # Serialization rules
    serialize_rules = ('-workout_exercises.exercise',)
    
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 2:
            raise ValueError("Exercise name must be at least 2 characters long")
        return name
    
    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['Cardio', 'Strength', 'Flexibility', 'Balance']
        if category not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return category

class WorkoutExercise(db.Model, SerializerMixin):
    __tablename__ = 'workout_exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    
    # User-submittable attributes
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight = db.Column(db.Float)
    duration = db.Column(db.Integer)
    distance = db.Column(db.Float)
    notes = db.Column(db.Text)
    order = db.Column(db.Integer)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Serialization rules
    serialize_rules = ('-user.workouts', '-user.progress_logs', '-user.workout_exercises',
                      '-workout.workout_exercises', '-exercise.workout_exercises')
    
    @validates('sets')
    def validate_sets(self, key, sets):
        if sets is not None and sets < 0:
            raise ValueError("Sets cannot be negative")
        return sets
    
    @validates('reps')
    def validate_reps(self, key, reps):
        if reps is not None and reps < 0:
            raise ValueError("Reps cannot be negative")
        return reps

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
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Serialization rules
    serialize_rules = ('-user.workouts', '-user.progress_logs', '-user.workout_exercises')
    
    @validates('weight')
    def validate_weight(self, key, weight):
        if weight is not None and weight < 0:
            raise ValueError("Weight cannot be negative")
        return weight
    
    @validates('log_date')
    def validate_log_date(self, key, log_date):
        if log_date > datetime.now().date():
            raise ValueError("Log date cannot be in the future")
        return log_date