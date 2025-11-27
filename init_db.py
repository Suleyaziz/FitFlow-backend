# init_db.py
from run import app  # Import from run.py
from models import db

with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully!")