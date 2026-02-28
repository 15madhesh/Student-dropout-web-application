import sqlite3
import os
from app import app

# Check current database location
print("Current working directory:", os.getcwd())
print("Instance directory exists:", os.path.exists('instance'))

# Check the database file in instance/
db_path = 'instance/students.db'
print("Database file exists:", os.path.exists(db_path))

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if student table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='student'")
    table_exists = cursor.fetchone()
    print("Student table exists:", table_exists is not None)
    
    if table_exists:
        # Check columns in student table
        cursor.execute("PRAGMA table_info(student)")
        columns = cursor.fetchall()
        print("\nStudent table columns:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        # Check if gender column exists
        gender_exists = any(col[1] == 'gender' for col in columns)
        print("\nGender column exists:", gender_exists)
        
        if not gender_exists:
            print("Adding gender column...")
            cursor.execute("ALTER TABLE student ADD COLUMN gender TEXT")
            conn.commit()
            print("Gender column added successfully!")
    else:
        print("Creating student table with all columns...")
        # Create the table with all required columns including gender
        cursor.execute('''
            CREATE TABLE student (
                id INTEGER PRIMARY KEY,
                username TEXT,
                stud_name TEXT,
                gender TEXT,
                dob TEXT,
                status TEXT,
                sslc_marks TEXT,
                hsc_marks TEXT,
                clg_name TEXT,
                mother_name TEXT,
                father_name TEXT,
                address TEXT
            )
        ''')
        conn.commit()
        print("Student table created successfully with gender column!")
    
    conn.close()
else:
    print("Creating new database with student table...")
    os.makedirs('instance', exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE student (
            id INTEGER PRIMARY KEY,
            username TEXT,
            stud_name TEXT,
            gender TEXT,
            dob TEXT,
            status TEXT,
            sslc_marks TEXT,
            hsc_marks TEXT,
            clg_name TEXT,
            mother_name TEXT,
            father_name TEXT,
            address TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("New database created successfully with gender column!")

# Also check the root students.db
root_db_path = 'students.db'
if os.path.exists(root_db_path):
    print(f"\nFound students.db in root directory - this might be interfering")
    conn = sqlite3.connect(root_db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='student'")
    root_table_exists = cursor.fetchone()
    if root_table_exists:
        cursor.execute("PRAGMA table_info(student)")
        root_columns = cursor.fetchall()
        print("Root students.db columns:")
        for col in root_columns:
            print(f"  {col[1]} ({col[2]})")
    conn.close()