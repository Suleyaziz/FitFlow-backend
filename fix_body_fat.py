# fix_body_fat.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from sqlalchemy import text

def add_body_fat_column():
    app = create_app()
    
    with app.app_context():
        try:
            print("🔍 Checking database and progress_logs table...")
            
            # First, list all tables to verify connection
            result = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = [row[0] for row in result.fetchall()]
            print(f"📊 Tables in database: {tables}")
            
            if 'progress_logs' in tables:
                # Check current columns in progress_logs
                result = db.session.execute(text("PRAGMA table_info(progress_logs);"))
                columns = [row[1] for row in result.fetchall()]
                print(f"📋 Current columns in progress_logs: {columns}")
                
                if 'body_fat' not in columns:
                    print("➕ Adding body_fat column...")
                    db.session.execute(text('ALTER TABLE progress_logs ADD COLUMN body_fat REAL'))
                    db.session.commit()
                    print("✅ body_fat column added successfully!")
                    
                    # Verify it was added
                    result = db.session.execute(text("PRAGMA table_info(progress_logs);"))
                    columns_after = [row[1] for row in result.fetchall()]
                    print(f"📋 Columns after update: {columns_after}")
                else:
                    print("✅ body_fat column already exists")
            else:
                print("❌ progress_logs table not found in database")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()

if __name__ == '__main__':
    add_body_fat_column()