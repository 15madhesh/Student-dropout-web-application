#!/usr/bin/env python3
"""
Migration script to transfer data from SQLite to MySQL 8.0
This script will:
1. Connect to the existing SQLite database
2. Create MySQL databases and tables
3. Transfer all data from SQLite to MySQL
"""

import sqlite3
import pymysql
from datetime import datetime
import os

# MySQL configuration - adjust as needed
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'vaibav@006',
    'port': 3306
}

def connect_mysql():
    """Connect to MySQL without specifying a database"""
    return pymysql.connect(
        host=MYSQL_CONFIG['host'],
        user=MYSQL_CONFIG['user'],
        password=MYSQL_CONFIG['password'],
        port=MYSQL_CONFIG['port'],
        charset='utf8mb4'
    )

def connect_mysql_db(db_name):
    """Connect to specific MySQL database"""
    return pymysql.connect(
        host=MYSQL_CONFIG['host'],
        user=MYSQL_CONFIG['user'],
        password=MYSQL_CONFIG['password'],
        port=MYSQL_CONFIG['port'],
        database=db_name,
        charset='utf8mb4'
    )

def create_mysql_databases():
    """Create MySQL databases"""
    conn = connect_mysql()
    cursor = conn.cursor()
    
    # Create databases
    cursor.execute("CREATE DATABASE IF NOT EXISTS students_db")
    cursor.execute("CREATE DATABASE IF NOT EXISTS dropout_students_db")
    
    # Grant privileges
    cursor.execute("GRANT ALL PRIVILEGES ON students_db.* TO 'root'@'localhost'")
    cursor.execute("GRANT ALL PRIVILEGES ON dropout_students_db.* TO 'root'@'localhost'")
    cursor.execute("FLUSH PRIVILEGES")
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ MySQL databases created successfully")

def create_mysql_tables():
    """Create MySQL tables with proper schema"""
    # Students database
    conn = connect_mysql_db('students_db')
    cursor = conn.cursor()
    
    # Create student table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(150) NOT NULL UNIQUE,
            stud_name VARCHAR(150) NOT NULL,
            gender VARCHAR(10),
            dob DATE,
            status VARCHAR(100),
            sslc_marks VARCHAR(10),
            hsc_marks VARCHAR(10),
            clg_name VARCHAR(150),
            mother_name VARCHAR(150),
            father_name VARCHAR(150),
            address TEXT
        )
    """)
    
    # Create university_marks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS university_marks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT NOT NULL,
            semester INT NOT NULL,
            internal1_sub1 FLOAT DEFAULT 0,
            internal1_sub2 FLOAT DEFAULT 0,
            internal1_sub3 FLOAT DEFAULT 0,
            internal1_sub4 FLOAT DEFAULT 0,
            internal1_sub5 FLOAT DEFAULT 0,
            internal1_sub6 FLOAT DEFAULT 0,
            internal2_sub1 FLOAT DEFAULT 0,
            internal2_sub2 FLOAT DEFAULT 0,
            internal2_sub3 FLOAT DEFAULT 0,
            internal2_sub4 FLOAT DEFAULT 0,
            internal2_sub5 FLOAT DEFAULT 0,
            internal2_sub6 FLOAT DEFAULT 0,
            internal3_sub1 FLOAT DEFAULT 0,
            internal3_sub2 FLOAT DEFAULT 0,
            internal3_sub3 FLOAT DEFAULT 0,
            internal3_sub4 FLOAT DEFAULT 0,
            internal3_sub5 FLOAT DEFAULT 0,
            internal3_sub6 FLOAT DEFAULT 0,
            cgpa FLOAT,
            FOREIGN KEY (student_id) REFERENCES student(id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    # Dropout students database
    conn = connect_mysql_db('dropout_students_db')
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dropout_students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(150) NOT NULL,
            stud_name VARCHAR(150) NOT NULL,
            gender VARCHAR(10),
            dob DATE,
            status VARCHAR(100),
            sslc_marks VARCHAR(10),
            hsc_marks VARCHAR(10),
            clg_name VARCHAR(150),
            mother_name VARCHAR(150),
            father_name VARCHAR(150),
            address TEXT,
            dropout_reason VARCHAR(255),
            dropout_date DATE
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ MySQL tables created successfully")

def migrate_student_data():
    """Migrate student data from SQLite to MySQL"""
    # Connect to SQLite
    sqlite_conn = sqlite3.connect('instance/students.db')
    sqlite_cursor = sqlite_conn.cursor()
    
    # Connect to MySQL
    mysql_conn = connect_mysql_db('students_db')
    mysql_cursor = mysql_conn.cursor()
    
    # Get all students from SQLite
    sqlite_cursor.execute("SELECT * FROM student")
    students = sqlite_cursor.fetchall()
    
    # Get column names
    sqlite_cursor.execute("PRAGMA table_info(student)")
    columns = [col[1] for col in sqlite_cursor.fetchall()]
    
    # Insert students into MySQL
    if students:
        placeholders = ', '.join(['%s'] * len(columns))
        columns_str = ', '.join(columns)
        
        for student in students:
            # Handle NULL values and convert date strings
            student_data = []
            for value in student:
                if value == 'NULL' or value is None:
                    student_data.append(None)
                elif isinstance(value, str) and len(value) == 10 and value.count('-') == 2:
                    # Convert date string to proper format
                    try:
                        student_data.append(datetime.strptime(value, '%Y-%m-%d').date())
                    except:
                        student_data.append(value)
                else:
                    student_data.append(value)
            
            mysql_cursor.execute(
                f"INSERT INTO student ({columns_str}) VALUES ({placeholders})",
                student_data
            )
    
    mysql_conn.commit()
    print(f"✅ Migrated {len(students)} students to MySQL")
    
    # Migrate university marks
    sqlite_cursor.execute("SELECT * FROM university_marks")
    marks = sqlite_cursor.fetchall()
    
    if marks:
        sqlite_cursor.execute("PRAGMA table_info(university_marks)")
        mark_columns = [col[1] for col in sqlite_cursor.fetchall()]
        
        placeholders = ', '.join(['%s'] * len(mark_columns))
        columns_str = ', '.join(mark_columns)
        
        for mark in marks:
            mark_data = []
            for value in mark:
                if value == 'NULL' or value is None:
                    mark_data.append(None)
                else:
                    mark_data.append(value)
            
            mysql_cursor.execute(
                f"INSERT INTO university_marks ({columns_str}) VALUES ({placeholders})",
                mark_data
            )
    
    mysql_conn.commit()
    print(f"✅ Migrated {len(marks)} university marks records to MySQL")
    
    # Close connections
    sqlite_cursor.close()
    sqlite_conn.close()
    mysql_cursor.close()
    mysql_conn.close()

def main():
    """Main migration function"""
    print("🔄 Starting SQLite to MySQL migration...")
    print("📊 Checking source database...")
    
    # Check if SQLite database exists
    if not os.path.exists('instance/students.db'):
        print("❌ SQLite database not found at instance/students.db")
        return
    
    try:
        # Step 1: Create MySQL databases
        print("1️⃣ Creating MySQL databases...")
        create_mysql_databases()
        
        # Step 2: Create MySQL tables
        print("2️⃣ Creating MySQL tables...")
        create_mysql_tables()
        
        # Step 3: Migrate data
        print("3️⃣ Migrating data from SQLite to MySQL...")
        migrate_student_data()
        
        print("🎉 Migration completed successfully!")
        print("\nNext steps:")
        print("1. Install PyMySQL: pip install pymysql")
        print("2. Install MySQL server if not already installed")
        print("3. Update database credentials in app.py if needed")
        print("4. Run the application")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        print("Please check:")
        print("1. MySQL server is running")
        print("2. Connection credentials are correct")
        print("3. Required packages are installed")

if __name__ == "__main__":
    main()