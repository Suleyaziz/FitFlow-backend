# init_db.py - improved version
from run import app
from models import db
from sqlalchemy import text

with app.app_context():
    try:
        # This will create any missing tables
        db.create_all()
        print("✅ Database tables verified/created successfully!")
        
        # Check if body_fat column exists in progress_logs
        result = db.session.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='progress_logs' AND column_name='body_fat'
        """))
        
        if not result.fetchone():
            # Add the missing column
            db.session.execute(text('ALTER TABLE progress_logs ADD COLUMN body_fat REAL'))
            db.session.commit()
            print("✅ Added body_fat column to progress_logs")
        else:
            print("✅ body_fat column already exists")
            
    except Exception as e:
        print(f"⚠️ Database initialization note: {e}")