import sqlite3

def add_attendance_column(db_path='dropout-analyzer/students.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE student ADD COLUMN attendance_percent FLOAT DEFAULT 0")
        print("Column 'attendance_percent' added successfully.")
    except sqlite3.OperationalError as e:
        if 'duplicate column name' in str(e).lower():
            print("Column 'attendance_percent' already exists.")
        else:
            print(f"Error occurred: {e}")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_attendance_column()
