import sqlite3
import os

# Get absolute path to the database
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'students.db')
instance_path = os.path.join(current_dir, 'instance', 'students.db')

print(f"Checking main database at: {db_path}")
print(f"Database exists: {os.path.exists(db_path)}")

# Check both databases
for path, name in [(db_path, 'main'), (instance_path, 'instance')]:
    print(f"\n=== {name.upper()} DATABASE ===")
    print(f"Path: {path}")
    print(f"Exists: {os.path.exists(path)}")
    
    if os.path.exists(path):
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tables found: {tables}")
        
        # Check each table
        for table_name, in tables:
            print(f"\n--- TABLE: {table_name} ---")
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print("Columns:")
            for col in columns:
                print(f"  {col[0]}: {col[1]} ({col[2]})")
        
        # Check specific for student table
        if any(table[0] == 'student' for table in tables):
            cursor.execute("PRAGMA table_info(student)")
            student_columns = cursor.fetchall()
            gender_exists = any(col[1] == 'gender' for col in student_columns)
            print(f"\nGender column exists: {gender_exists}")
            if gender_exists:
                print("✅ Database schema is correct!")
        
        conn.close()

# Create a fresh database with proper schema
print("\n=== CREATING FRESH DATABASE ===")
from app import db, app

with app.app_context():
    try:
        db.create_all()
        print("✅ All tables created successfully via SQLAlchemy")
        
        # Verify
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("Created tables:", tables)
        
        if any(t[0] == 'student' for t in tables):
            cursor.execute("PRAGMA table_info(student)")
            cols = cursor.fetchall()
            print("Student columns:", [c[1] for c in cols])
        
        conn.close()
        
    except Exception as e:
        print("Error:", e)