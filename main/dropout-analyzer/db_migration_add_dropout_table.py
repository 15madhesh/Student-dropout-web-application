from dropout_analyzer.app import db
from sqlalchemy import Column, Integer, Boolean, String, Text, ForeignKey

def upgrade():
    # Create DropoutStudentDetails table
    db.engine.execute("""
    CREATE TABLE IF NOT EXISTS dropout_student_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER UNIQUE,
        disciplinary_action BOOLEAN DEFAULT 0,
        family_income VARCHAR(100),
        fees_payment_status VARCHAR(20),
        educational_load BOOLEAN DEFAULT 0,
        part_time_work BOOLEAN DEFAULT 0,
        health_issue BOOLEAN DEFAULT 0,
        health_issue_description TEXT,
        day_scholar_or_hosteller VARCHAR(20),
        FOREIGN KEY(student_id) REFERENCES student(id)
    );
    """)

def downgrade():
    # Drop DropoutStudentDetails table
    db.engine.execute("DROP TABLE IF EXISTS dropout_student_details;")

if __name__ == "__main__":
    upgrade()
