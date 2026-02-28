import sqlite3
import json

def dump_student_marks(student_id, db_path='dropout-analyzer/students.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch student info
    cursor.execute("SELECT id, username, stud_name, attendance_percent FROM student WHERE id=?", (student_id,))
    student = cursor.fetchone()
    if not student:
        print(f"No student found with id {student_id}")
        return

    student_info = {
        'id': student[0],
        'username': student[1],
        'stud_name': student[2],
        'attendance_percent': student[3] if len(student) > 3 else None
    }

    # Fetch marks
    cursor.execute("""
        SELECT semester, internal1_sub1, internal1_sub2, internal1_sub3, internal1_sub4, internal1_sub5, internal1_sub6,
               internal2_sub1, internal2_sub2, internal2_sub3, internal2_sub4, internal2_sub5, internal2_sub6,
               internal3_sub1, internal3_sub2, internal3_sub3, internal3_sub4, internal3_sub5, internal3_sub6,
               cgpa
        FROM university_marks
        WHERE student_id=?
    """, (student_id,))
    marks_rows = cursor.fetchall()

    marks = []
    for row in marks_rows:
        marks.append({
            'semester': row[0],
            'internal1_sub1': row[1],
            'internal1_sub2': row[2],
            'internal1_sub3': row[3],
            'internal1_sub4': row[4],
            'internal1_sub5': row[5],
            'internal1_sub6': row[6],
            'internal2_sub1': row[7],
            'internal2_sub2': row[8],
            'internal2_sub3': row[9],
            'internal2_sub4': row[10],
            'internal2_sub5': row[11],
            'internal2_sub6': row[12],
            'internal3_sub1': row[13],
            'internal3_sub2': row[14],
            'internal3_sub3': row[15],
            'internal3_sub4': row[16],
            'internal3_sub5': row[17],
            'internal3_sub6': row[18],
            'cgpa': row[19]
        })

    result = {
        'student': student_info,
        'marks': marks
    }

    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    # Replace with the student ID you want to inspect
    dump_student_marks(1)
