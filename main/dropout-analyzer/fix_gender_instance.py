#!/usr/bin/env python3
"""
Script to fix the missing gender column in the student table (instance folder)
"""

import sqlite3
import os

def fix_gender_column():
    """Add the missing gender column to the student table in instance folder"""
    db_path = 'instance/students.db'
    
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check current columns
        cursor.execute('PRAGMA table_info(student)')
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print("Current student table columns:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        # Add gender column if it doesn't exist
        if 'gender' not in column_names:
            cursor.execute('ALTER TABLE student ADD COLUMN gender TEXT')
            conn.commit()
            print("✅ Successfully added 'gender' column to student table")
        else:
            print("✅ 'gender' column already exists")
            
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("✅ 'gender' column already exists")
        else:
            print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    fix_gender_column()
