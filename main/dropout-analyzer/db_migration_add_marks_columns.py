import sqlite3
import os

def migrate_university_marks():
    """Add missing columns to university_marks table"""
    db_path = 'students.db'

    if not os.path.exists(db_path):
        print(f"Database {db_path} not found!")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if university_marks table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='university_marks'")
        if not cursor.fetchone():
            print("university_marks table does not exist!")
            conn.close()
            return False

        # Get existing columns
        cursor.execute("PRAGMA table_info(university_marks)")
        existing_columns = [row[1] for row in cursor.fetchall()]
        print(f"Existing columns: {existing_columns}")

        # Columns to add
        columns_to_add = [
            'internal1_sub1', 'internal1_sub2', 'internal1_sub3', 'internal1_sub4', 'internal1_sub5', 'internal1_sub6',
            'internal2_sub1', 'internal2_sub2', 'internal2_sub3', 'internal2_sub4', 'internal2_sub5', 'internal2_sub6',
            'internal3_sub1', 'internal3_sub2', 'internal3_sub3', 'internal3_sub4', 'internal3_sub5', 'internal3_sub6',
            'cgpa'
        ]

        added_count = 0
        for column in columns_to_add:
            if column not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE university_marks ADD COLUMN {column} FLOAT")
                    print(f"✅ Added column {column}")
                    added_count += 1
                except Exception as e:
                    print(f"❌ Failed to add column {column}: {e}")
            else:
                print(f"⚠️ Column {column} already exists")

        conn.commit()
        conn.close()

        print(f"✅ Migration completed. Added {added_count} columns.")
        return True

    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return False

if __name__ == "__main__":
    migrate_university_marks()
