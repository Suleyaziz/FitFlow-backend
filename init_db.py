from app import app
from models import db, User  # Import your models

with app.app_context():
    db.create_all()
    print("Database tables created!")