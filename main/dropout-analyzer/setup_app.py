#!/usr/bin/env python3
"""
Automated setup script for MySQL migration
This script runs automatically when app.py starts to ensure MySQL is ready
"""

import os
import sys
import subprocess
import importlib.util
import time

def check_mysql_installed():
    """Check if MySQL is installed and accessible"""
    try:
        import pymysql
        return True
    except ImportError:
        return False

def check_mysql_running():
    """Check if MySQL server is running"""
    try:
        import pymysql
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            port=3306,
            connect_timeout=5
        )
        conn.close()
        return True
    except:
        return False

def install_mysql_driver():
    """Install required MySQL packages"""
    print("Installing MySQL driver...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pymysql", "cryptography"], check=True)

def setup_mysql():
    """Setup MySQL databases and tables"""
    try:
        import pymysql
        
        # Create databases
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            port=3306
        )
        cursor = conn.cursor()
        
        cursor.execute("CREATE DATABASE IF NOT EXISTS students_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute("CREATE DATABASE IF NOT EXISTS dropout_students_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        # Create tables
        conn.select_db('students_db')
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
        
        conn.select_db('dropout_students_db')
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
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error setting up MySQL: {e}")
        return False

def migrate_data_if_needed():
    """Migrate data from SQLite to MySQL if MySQL is empty and SQLite has data"""
    try:
        import pymysql
        
        # Check if MySQL has data
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            port=3306,
            database='students_db'
        )
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM student")
        mysql_count = cursor.fetchone()[0]
        conn.close()
        
        if mysql_count > 0:
            print("✅ MySQL already has data")
            return True
        
        # Check if SQLite has data
        import sqlite3
        if os.path.exists('instance/students.db'):
            sqlite_conn = sqlite3.connect('instance/students.db')
            sqlite_cursor = sqlite_conn.cursor()
            
            sqlite_cursor.execute("SELECT COUNT(*) FROM student")
            sqlite_count = sqlite_cursor.fetchone()[0]
            sqlite_conn.close()
            
            if sqlite_count > 0:
                print(f"Found {sqlite_count} records in SQLite, migrating to MySQL...")
                # Import and run migration
                if os.path.exists('migrate_to_mysql.py'):
                    subprocess.run([sys.executable, "migrate_to_mysql.py"], check=True)
                    return True
        
        return True
        
    except Exception as e:
        print(f"Error during data migration: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up MySQL for Dropout Analyzer...")
    
    # Check if MySQL driver is installed
    if not check_mysql_installed():
        print("Installing MySQL driver...")
        install_mysql_driver()
    
    # Check MySQL connection
    if not check_mysql_running():
        print("❌ MySQL server is not running. Please start MySQL server first.")
        print("   Windows: net start mysql80")
        print("   Linux: sudo service mysql start")
        return False
    
    # Setup MySQL databases and tables
    if not setup_mysql():
        print("❌ Failed to setup MySQL databases")
        return False
    
    # Migrate data if needed
    migrate_data_if_needed()
    
    print("✅ MySQL setup complete!")
    return True

if __name__ == "__main__":
    main()