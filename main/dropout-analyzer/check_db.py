import sqlite3
import os

# Check the actual students.db in current directory
db_path = 'students.db'
print(f"Checking database: {db_path}")
print(f"File exists: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"Tables found: {tables}")
    
    # Check each table
    for table_name, in tables:
        print(f"\n--- Table: {table_name} ---")
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
    
    conn.close()
else:
    print("Database file does not exist!")