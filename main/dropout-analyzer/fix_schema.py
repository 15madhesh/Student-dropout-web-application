#!/usr/bin/env python3
import sqlite3
import os

def fix_gender_column():
    """Add missing gender column to student table"""
    db_path = 'students.db'
    
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if gender column already exists
        cursor.execute("PRAGMA table_info(student)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'gender' not in columns:
            print("Adding gender column...")
            cursor.execute("ALTER TABLE student ADD COLUMN gender VARCHAR(10)")
            conn.commit()
            print("✅ Gender column added successfully!")
        else:
            print("✅ Gender column already exists")
            
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    fix_gender_column()
