# SQLite to MySQL 8.0 Migration Guide

This guide will help you migrate your dropout analyzer application from SQLite to MySQL 8.0.

## Prerequisites

1. **MySQL Server 8.0** must be installed and running
2. **MySQL Command Line Client** must be accessible from your terminal
3. **Python packages** must be installed (`pymysql`, `cryptography`)

## Quick Start

### Step 1: Install MySQL Requirements
```bash
pip install -r requirements_mysql.txt
```

### Step 2: Create MySQL Databases and Tables

#### Method 1: Using MySQL Command Line Client
```bash
# Open MySQL command line client
mysql -u root -p

# Then run the SQL script
source setup_mysql.sql
```

#### Method 2: Using MySQL Workbench
1. Open MySQL Workbench
2. Connect to your local MySQL server
3. Open and execute `setup_mysql.sql`

### Step 3: Update Database Credentials (if needed)

The application is configured with default credentials:
- **Username**: root
- **Password**: password  
- **Host**: localhost
- **Port**: 3306

If your MySQL setup is different, edit `app.py`:
```python
# Update these lines in app.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://YOUR_USERNAME:YOUR_PASSWORD@localhost:3306/students_db'
app.config['SQLALCHEMY_BINDS'] = {
    'dropout': 'mysql+pymysql://YOUR_USERNAME:YOUR_PASSWORD@localhost:3306/dropout_students_db'
}
```

### Step 4: Migrate Data from SQLite to MySQL

```bash
# Run the migration script
python migrate_to_mysql.py
```

## Manual Setup Instructions

### 1. Create Databases Manually

```sql
-- In MySQL command line client:
CREATE DATABASE IF NOT EXISTS students_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS dropout_students_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Create Tables

```sql
USE students_db;

CREATE TABLE student (
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
);

CREATE TABLE university_marks (
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
);

USE dropout_students_db;

CREATE TABLE dropout_students (
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
);
```

## Troubleshooting

### Common Issues

1. **MySQL Connection Error**
   - Ensure MySQL service is running: `net start mysql80` (Windows) or `sudo service mysql start` (Linux)
   - Check if MySQL is listening on port 3306: `netstat -an | findstr 3306`

2. **Authentication Error**
   - Reset MySQL root password:
     ```bash
     mysql -u root -p
     ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';
     FLUSH PRIVILEGES;
     ```

3. **Import Error for pymysql**
   - Install with: `pip install pymysql cryptography`

### Testing the Migration

After completing the migration:

1. **Test MySQL connection**:
```bash
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('✅ MySQL connection successful')
"
```

2. **Verify data**:
```bash
python -c "
from app import app, db, Student
with app.app_context():
    students = Student.query.all()
    print(f'✅ Found {len(students)} students in MySQL')
"
```

## Backup Information

### Original SQLite Database
- **Location**: `instance/students.db`
- **Backup**: Make a copy before migration

### Rollback Plan
To rollback to SQLite:
1. Change `app.py` back to:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_BINDS'] = {
    'dropout': 'sqlite:///dropout_students.db'
}
```

## Performance Optimizations

After migration, you may want to:
1. Add indexes for frequently queried columns
2. Adjust MySQL configuration for better performance
3. Use connection pooling for production

## Support

If you encounter issues:
1. Check MySQL error logs
2. Verify database credentials
3. Ensure all required packages are installed
4. Check firewall settings if connecting remotely