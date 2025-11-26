from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

# -----------------------
# User model
# -----------------------
class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Fitness profile
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    fitness_goal = db.Column(db.String(200))
    target_weight = db.Column(db.Float)

    workouts = db.relationship("Workout", backref="user", cascade="all, delete-orphan", lazy=True)
    progress_logs = db.relationship("ProgressLog", backref="user", cascade="all, delete-orphan", lazy=True)
    workout_exercises = db.relationship("WorkoutExercise", backref="user", cascade="all, delete-orphan", lazy=True)

    # FIXED: Remove circular references
    serialize_rules = ('-password_hash', '-workouts.user', '-progress_logs.user', '-workout_exercises.user', '-workouts.workout_exercises.workout')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Add a simple to_dict method for auth responses
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'fitness_goal': self.fitness_goal,
            'target_weight': self.target_weight
        }

    @validates("username")
    def validate_username(self, key, username):
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        return username

    @validates("email")
    def validate_email(self, key, email):
        if not email or "@" not in email:
            raise ValueError("Invalid email")
        return email

# -----------------------
# Workout model
# -----------------------
class Workout(db.Model, SerializerMixin):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    duration = db.Column(db.Integer)
    calories_burned = db.Column(db.Float)
    workout_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    workout_exercises = db.relationship("WorkoutExercise", backref="workout", cascade="all, delete-orphan", lazy=True)
    
    # FIXED: Simplify serialize rules
    serialize_rules = ('-user.workouts', '-workout_exercises.workout', '-workout_exercises.user')

# -----------------------
# Exercise model
# -----------------------
class Exercise(db.Model, SerializerMixin):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    muscle_group = db.Column(db.String(80))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    workout_exercises = db.relationship("WorkoutExercise", backref="exercise", cascade="all, delete-orphan", lazy=True)
    
    # FIXED: Simplify
    serialize_rules = ('-workout_exercises.exercise',)

# -----------------------
# WorkoutExercise model
# -----------------------
class WorkoutExercise(db.Model, SerializerMixin):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)

    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight = db.Column(db.Float)
    duration = db.Column(db.Integer)
    distance = db.Column(db.Float)
    notes = db.Column(db.Text)
    order = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # FIXED: Remove circular references
    serialize_rules = ('-user.workout_exercises', '-workout.workout_exercises', '-exercise.workout_exercises')

# -----------------------
# ProgressLog model
# -----------------------
class ProgressLog(db.Model, SerializerMixin):
    __tablename__ = "progress_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    log_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    weight = db.Column(db.Float)
    chest = db.Column(db.Float)
    waist = db.Column(db.Float)
    hips = db.Column(db.Float)
    biceps = db.Column(db.Float)
    thighs = db.Column(db.Float)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # FIXED: Simplify
    serialize_rules = ('-user.progress_logs',)