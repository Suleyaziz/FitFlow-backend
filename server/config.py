import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fitflow-secret-key-2024")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fitflow-jwt-secret-key-2024")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'instance', 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
