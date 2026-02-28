-- Create databases for the application
CREATE DATABASE IF NOT EXISTS students_db;
CREATE DATABASE IF NOT EXISTS dropout_students_db;

-- Grant privileges (adjust username and password as needed)
GRANT ALL PRIVILEGES ON students_db.* TO 'root'@'localhost';
GRANT ALL PRIVILEGES ON dropout_students_db.* TO 'root'@'localhost';

FLUSH PRIVILEGES;

-- Use the main database
USE students_db;

-- Create student table
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
);

-- Create university_marks table
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
);

-- Create dropout_students table in dropout_students_db
USE dropout_students_db;
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
);