# server/routes/__init__.py
from flask_restful import Api

# Import all resource classes
from server.routes.users import (
    UserRegisterResource,
    UserLoginResource,
    UserLogoutResource,
    UserResource,
)
from server.routes.workouts import WorkoutResource
from server.routes.exercises import ExerciseResource
from server.routes.workout_exercises import WorkoutExerciseResource
from server.routes.progress_logs import ProgressLogResource
from server.routes.auth import RegisterAPI, LoginAPI

def register_routes(api: Api):
    """Register all API routes"""
    
    # Auth routes
    api.add_resource(RegisterAPI, "/register")
    api.add_resource(LoginAPI, "/login")

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
