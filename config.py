import os

# Only load .env file in development, not production
if os.getenv('FLASK_ENV') != 'production':
    from dotenv import load_dotenv
    load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fitflow-secret-key-2024")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fitflow-jwt-secret-key-2024")
    
    # FIXED: Handle both Render PostgreSQL and local SQLite
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        # Fix Render PostgreSQL URL format
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Fallback to SQLite for local development - CORRECTED PATH
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'server', 'instance', 'app.db')}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False