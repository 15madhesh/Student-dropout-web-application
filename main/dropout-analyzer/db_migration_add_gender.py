import sqlite3

def upgrade():
    conn = sqlite3.connect('instance/students.db')
    cursor = conn.cursor()
    
    try:
        # Add gender column to student table
        cursor.execute("ALTER TABLE student ADD COLUMN gender TEXT")
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"Error adding gender column: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    upgrade()