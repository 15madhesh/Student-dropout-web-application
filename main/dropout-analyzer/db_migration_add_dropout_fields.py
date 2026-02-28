import sqlite3

def migrate():
    conn = sqlite3.connect('dropout-analyzer/students.db')
    cursor = conn.cursor()

    # Add new columns to student table if they don't exist
    columns = {
        'disciplinary_action': 'INTEGER DEFAULT 0',
        'family_income': 'TEXT',
        'fees_payment_status': 'TEXT',
        'educational_load': 'INTEGER DEFAULT 0',
        'part_time_work': 'INTEGER DEFAULT 0',
        'health_issue': 'INTEGER DEFAULT 0',
        'health_issue_description': 'TEXT',
        'day_scholar_or_hosteller': 'TEXT'
    }

    # Get existing columns
    cursor.execute("PRAGMA table_info(student)")
    existing_columns = [info[1] for info in cursor.fetchall()]

    for column, col_type in columns.items():
        if column not in existing_columns:
            try:
                cursor.execute(f"ALTER TABLE student ADD COLUMN {column} {col_type}")
                print(f"Added column {column}")
            except Exception as e:
                print(f"Failed to add column {column}: {e}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()
