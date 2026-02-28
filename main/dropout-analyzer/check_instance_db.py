import sqlite3
import os

db_path = 'instance/students.db'
print(f"Checking database: {db_path}")
print(f"File exists: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"Tables found: {tables}")

    # Check university_marks table
    if ('university_marks',) in tables:
        print("\n--- Table: university_marks ---")
        cursor.execute("PRAGMA table_info(university_marks)")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
    else:
        print("university_marks table not found")

    conn.close()
else:
    print("Database file does not exist!")
