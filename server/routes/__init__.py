# server/routes/__init__.py
from flask_restful import Api

# Import all resource classes
from routes.users import (
    UserRegisterResource,
    UserLoginResource,
    UserLogoutResource,
    UserResource,
)
from routes.workouts import WorkoutResource
from routes.exercises import ExerciseResource
from routes.workout_exercises import WorkoutExerciseResource
from routes.progress_logs import ProgressLogResource
from routes.auth import RegisterAPI, LoginAPI, CurrentUserAPI



def register_routes(api: Api):
    """Register all API routes"""
    
    # Auth routes
    api.add_resource(RegisterAPI, "/register")
    api.add_resource(LoginAPI, "/login")
    api.add_resource(CurrentUserAPI, "/auth/me")

    # User routes (for profile management)
    api.add_resource(UserResource, "/users", "/users/<int:user_id>")

    # Workouts
    api.add_resource(WorkoutResource, "/workouts", "/workouts/<int:workout_id>")

    # Exercises
    api.add_resource(ExerciseResource, "/exercises", "/exercises/<int:exercise_id>")

    # WorkoutExercises
    api.add_resource(WorkoutExerciseResource, "/workout_exercises", "/workout_exercises/<int:we_id>")

    # Progress Logs (renamed to /progress for frontend compatibility)
    api.add_resource(ProgressLogResource, "/progress", "/progress/<int:log_id>")
