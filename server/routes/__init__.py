# routes/__init__.py
from flask_restful import Api

# REMOVE THIS LINE - it's causing the circular import!
# from app import create_app

# Use relative imports
from .users import (
    UserRegisterResource,
    UserLoginResource,
    UserLogoutResource,
    UserResource,
)
from .workouts import WorkoutResource
from .exercises import ExerciseResource
from .workout_exercises import WorkoutExerciseResource
from .progress_logs import ProgressLogResource
from .auth import RegisterAPI, LoginAPI, CurrentUserAPI

def register_routes(api: Api):
    """Register all API routes"""
    
    # Auth routes
    api.add_resource(RegisterAPI, "/register")
    api.add_resource(LoginAPI, "/login")
    api.add_resource(CurrentUserAPI, "/auth/me")  # ADDED: Fix missing endpoint

    # User routes
    api.add_resource(UserRegisterResource, "/users/register")
    api.add_resource(UserLoginResource, "/users/login")
    api.add_resource(UserLogoutResource, "/users/logout")
    api.add_resource(UserResource, "/users", "/users/<int:user_id>")

    # Workouts
    api.add_resource(WorkoutResource, "/workouts", "/workouts/<int:workout_id>")

    # Exercises
    api.add_resource(ExerciseResource, "/exercises", "/exercises/<int:exercise_id>")

    # WorkoutExercises
    api.add_resource(WorkoutExerciseResource, "/workout_exercises", "/workout_exercises/<int:we_id>")

    # ProgressLogs
    api.add_resource(ProgressLogResource, "/progress_logs", "/progress_logs/<int:log_id>")