from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database configuration
DB_PATH = '../dropout-analyzer/students.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    conn.close()
    return jsonify(dict(student)) if student else jsonify({'error': 'Student not found'}), 404

@app.route('/api/dropout-analysis', methods=['GET'])
def get_dropout_analysis():
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM dropout_analysis')
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(port=5001)