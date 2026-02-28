from flask import Flask, render_template, request, redirect, url_for, session
import os
from model import analyze_dropout
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_BINDS'] = {
    'dropout': 'sqlite:///dropout_students.db'
}
db = SQLAlchemy(app)

import pickle
from sqlalchemy import LargeBinary

class UniversityMarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    semester = db.Column(db.Integer)

    internal1 = db.Column(LargeBinary)
    internal2 = db.Column(LargeBinary)
    internal3 = db.Column(LargeBinary)

    cgpa = db.Column(db.Float)

    def get_internal_marks(self, internal_num):
        data = None
        if internal_num == 1:
            data = self.internal1
        elif internal_num == 2:
            data = self.internal2
        elif internal_num == 3:
            data = self.internal3
        if data:
            try:
                return pickle.loads(data)
            except Exception:
                return []
        return []

    def set_internal_marks(self, internal_num, marks_list):
        try:
            data = pickle.dumps(marks_list)
            if internal_num == 1:
                self.internal1 = data
            elif internal_num == 2:
                self.internal2 = data
            elif internal_num == 3:
                self.internal3 = data
        except Exception:
            pass

class DropoutStudentDetails(db.Model):
    __bind_key__ = 'dropout'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, unique=True)
    disciplinary_action = db.Column(db.Boolean, default=False)
    family_income = db.Column(db.String(100))
    fees_payment_status = db.Column(db.String(20))  # delayed, ontime, pending
    educational_load = db.Column(db.Boolean, default=False)
    part_time_work = db.Column(db.Boolean, default=False)
    health_issue = db.Column(db.Boolean, default=False)
    health_issue_description = db.Column(db.Text)
    day_scholar_or_hosteller = db.Column(db.String(20))  # day scholar or hosteller

# Removed duplicate route definition for dropout_students to fix AssertionError

@app.route('/update-marks', methods=['GET', 'POST'])

@app.route('/update_marks', methods=['GET', 'POST'])
def update_marks():
    if 'user' not in session:
        return redirect(url_for('login'))
    students = Student.query.filter_by(username=session['user']).all()
    if request.method == 'POST':
        student_id = request.form['student_id']
        semester = int(request.form['semester'])
        stage = request.form['stage']
        marks = [float(request.form.get(f'sub{i}', '0') or '0') for i in range(1, 7)]
        cgpa_input = request.form.get('cgpa', '')
        cgpa = float(cgpa_input) if cgpa_input.strip() else None

        record = UniversityMarks.query.filter_by(student_id=student_id, semester=semester).first()
        if not record:
            record = UniversityMarks(student_id=student_id, semester=semester)

        if stage == 'internal1':
            if record.internal1:
                return render_template('update_marks.html', students=students, error="Internal 1 marks already updated for this student and semester.")
            record.set_internal_marks(1, marks)
        elif stage == 'internal2':
            record.set_internal_marks(2, marks)
        elif stage == 'internal3':
            record.set_internal_marks(3, marks)
        elif stage == 'cgpa':
            record.cgpa = cgpa

        db.session.add(record)
        db.session.commit()
        return render_template('update_marks.html', students=students, success="Marks updated!")
    return render_template('update_marks.html', students=students)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    stud_name = db.Column(db.String(150))
    gender = db.Column(db.String(10))
    dob = db.Column(db.String(50))
    status = db.Column(db.String(100))
    sslc_marks = db.Column(db.String(10))
    hsc_marks = db.Column(db.String(10))
    clg_name = db.Column(db.String(150))
    mother_name = db.Column(db.String(150))
    father_name = db.Column(db.String(150))
    address = db.Column(db.Text)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
# ...existing code...
@app.route('/login', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check admin credentials
        if username == 'admin' and password == 'admin':
            session['user'] = username
            return redirect(url_for('dashboard'))
        # Check users.txt for other users
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    saved_user, saved_pass = line.strip().split(',', 1)
                    if username == saved_user and password == saved_pass:
                        session['user'] = username
                        return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid Credentials')
    return render_template('login.html')
# ...existing code...
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    # Get all student records for the logged-in user
    students = Student.query.filter_by(username=session['user']).all()
    return render_template('dashboard.html', students=students)
@app.route('/api/news')
def news_api():
    # News articles from mainstream news websites about education/dropouts
    news_items = [
        {
            "title": "Student drops out to start tea business, earns ₹5 crore/year",
            "url": "https://www.news18.com/viral/dropout-chaiwala",
            "image": "/static/images/news1.jpeg",
            "date": "2025-07-20"
        },
        {
            "title": "Rising dropout rates concern educators nationwide",
            "url": "https://timesofindia.indiatimes.com/topic/dropout-of-students",
            "image": "/static/images/news2.jpeg",
            "date": "2025-07-18"
        },
        {
            "title": "University introduces new program to retain students",
            "url": "https://www.hindustantimes.com/education/retention-program",
            "image": "/static/images/news3.jpeg",
            "date": "2025-07-15"
        },
        {
            "title": "Government announces scholarship for at-risk students",
            "url": "https://www.thehindu.com/search/#gsc.tab=0&gsc.q=dropout%20of%20students&gsc.sort=",
            "image": "/static/images/news4.jpeg",
            "date": "2025-07-12"
        },
        {
            "title": "Study links extracurriculars to lower dropout rates",
            "url": "https://indianexpress.com/education-study",
            "image": "/static/images/news5.jpeg",
            "date": "2025-07-10"
        },
        {
            "title": "College dropout builds edtech startup",
            "url": "https://economictimes.com/success-story",
            "image": "/static/images/news6.jpeg",
            "date": "2025-07-08"
        },
        {
            "title": "Alumni mentorship program reduces dropouts by 25%",
            "url": "https://www.deccanchronicle.com/mentorship-impact",
            "image": "/static/images/news7.jpeg",
            "date": "2025-07-05"
        },
        {
            "title": "Rural schools face increasing student attrition",
            "url": "https://www.thequint.com/rural-education",
            "image": "/static/images/news8.jpeg",
            "date": "2025-07-03"
        },
        {
            "title": "Online learning contributing to dropout crisis?",
            "url": "https://www.firstpost.com/online-education-impact",
            "image": "/static/images/news9.jpeg",
            "date": "2025-06-30"
        },
        {
            "title": "Vocational training helps retain disengaged students",
            "url": "https://www.financialexpress.com/vocational-success",
            "image": "/static/images/news10.jpeg",
            "date": "2025-06-28"
        },
        {
            "title": "Celebrity funds scholarship for dropout prevention",
            "url": "https://www.mid-day.com/celebrity-scholarship",
            "image": "/static/images/news11.jpeg",
            "date": "2025-06-25"
        },
        {
            "title": "New app connects at-risk students with counselors",
            "url": "https://www.livemint.com/edtech-app",
            "image": "/static/images/news12.jpeg",
            "date": "2025-06-22"
        }
    ]
    return jsonify(news_items)
    return render_template('dashboard.html', students=students)

@app.route('/dropout-students', methods=['GET', 'POST'])
def dropout_students():
    if 'user' not in session:
        return redirect(url_for('login'))
    students = Student.query.filter_by(username=session['user']).all()
    # Fetch dropout students as pairs (student, dropout_details)
    dropout_students = []
    all_dropout_details = DropoutStudentDetails.query.all()
    dropout_details_map = {d.student_id: d for d in all_dropout_details}
    for student in students:
        details = dropout_details_map.get(student.id)
        if details:
            dropout_students.append((student, details))
    # Calculate dropout counts grouped by college
    college_counts = {}
    for student, details in dropout_students:
        college = student.clg_name or "Unknown"
        college_counts[college] = college_counts.get(college, 0) + 1
    selected_student = None
    dropout_details = None
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        if student_id:
            selected_student = Student.query.filter_by(id=student_id, username=session['user']).first()
            if selected_student:
                dropout_details = DropoutStudentDetails.query.filter_by(student_id=selected_student.id).first()
                if not dropout_details:
                    dropout_details = DropoutStudentDetails(student_id=selected_student.id)
                dropout_details.disciplinary_action = request.form.get('disciplinary_action') == 'yes'
                dropout_details.family_income = request.form.get('family_income')
                dropout_details.fees_payment_status = request.form.get('fees_payment_status')
                dropout_details.educational_load = request.form.get('educational_load') == 'yes'
                dropout_details.part_time_work = request.form.get('part_time_work') == 'yes'
                dropout_details.health_issue = request.form.get('health_issue') == 'yes'
                dropout_details.health_issue_description = request.form.get('health_issue_description')
                dropout_details.day_scholar_or_hosteller = request.form.get('day_scholar_or_hosteller')
                db.session.add(dropout_details)
                # Update student status to 'dropout' after saving dropout details
                student = Student.query.filter_by(id=student_id, username=session['user']).first()
                if student:
                    student.status = 'dropout'
                    db.session.add(student)
                db.session.commit()
            # Add flash message to indicate update success
            from flask import flash
            flash('Dropout details saved and graph updated successfully.', 'success')
            return redirect(url_for('dropout_students', student_id=student_id))
    else:
        student_id = request.args.get('student_id')
        if student_id:
            selected_student = Student.query.filter_by(id=student_id, username=session['user']).first()
            if selected_student:
                dropout_details = DropoutStudentDetails.query.filter_by(student_id=selected_student.id).first()
    return render_template('dropout_students.html', students=students, dropout_students=dropout_students, selected_student=selected_student, dropout_details=dropout_details, college_counts=college_counts)

@app.route('/stats')
def stats():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('stats.html')

@app.route('/dropout-details')
def dropout_details():
    if 'user' not in session:
        return redirect(url_for('login'))
    students = Student.query.filter_by(username=session['user']).all()
    dropout_students = []
    all_dropout_details = DropoutStudentDetails.query.all()
    dropout_details_map = {d.student_id: d for d in all_dropout_details}
    for student in students:
        details = dropout_details_map.get(student.id)
        if details:
            dropout_students.append((student, details))
    return render_template('dropout_details.html', dropout_students=dropout_students)
@app.route('/signup', methods=['GET', 'POST'])

def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Save user to a file (simple demo, not secure)
        with open('users.txt', 'a') as f:
            f.write(f"{username},{password}\n")
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/about')
def about():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('about.html')

@app.route('/contact')
def contact():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('contact.html')

# ...existing code...
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files['file']
        if not allowed_file(file.filename):
            return render_template('upload.html', error='Only .txt or .csv files are allowed!')
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        result = analyze_dropout(filepath)
        return render_template('result.html', result=result)
    return render_template('upload.html')

@app.route('/solutions', methods=['GET', 'POST'])
def solutions():
    if 'user' not in session:
        return redirect(url_for('login'))
    students = Student.query.filter_by(username=session['user']).all()
    selected_student = None
    dropout_details = None
    if request.method == 'POST' and 'student_id' in request.form:
        student_id = request.form['student_id']
        selected_student = Student.query.get(student_id)
        # Get dropout details from separate table
        dropout_details = DropoutStudentDetails.query.filter_by(student_id=student_id).first()
        dropout_details = {
            'disciplinary_action': dropout_details.disciplinary_action if dropout_details else None,
            'family_income': dropout_details.family_income if dropout_details else None,
            'fees_payment_status': dropout_details.fees_payment_status if dropout_details else None,
            'educational_load': dropout_details.educational_load if dropout_details else None,
            'part_time_work': dropout_details.part_time_work if dropout_details else None,
            'health_issue': dropout_details.health_issue if dropout_details else None,
            'health_issue_description': dropout_details.health_issue_description if dropout_details else None,
            'day_scholar_or_hosteller': dropout_details.day_scholar_or_hosteller if dropout_details else None
        }
    return render_template('solutions.html',
                         students=students,
                         selected_student=selected_student,
                         dropout_details=dropout_details)
# ...existing code...
ALLOWED_EXTENSIONS = {'txt', 'csv'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# ...existing code...
@app.route('/manual-entry', methods=['GET', 'POST'])
def manual_entry():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        student = Student(
            username=session['user'],
            stud_name=request.form['stud_name'],
            gender=request.form['gender'],
            dob=request.form['dob'],
            status=request.form['status'],
            sslc_marks=request.form['sslc_marks'],
            hsc_marks=request.form['hsc_marks'],
            clg_name=request.form['clg_name'],
            mother_name=request.form['mother_name'],
            father_name=request.form['father_name'],
            address=request.form['address']
        )
        db.session.add(student)
        db.session.commit()
        # Pass all fields to analyze_dropout
        result = analyze_dropout({
            'stud_name': request.form['stud_name'],
            'dob': request.form['dob'],
            'status': request.form['status'],
            'sslc_marks': request.form['sslc_marks'],
            'hsc_marks': request.form['hsc_marks'],
            'clg_name': request.form['clg_name'],
            'mother_name': request.form['mother_name'],
            'father_name': request.form['father_name'],
            'address': request.form['address']
        }, manual=True)
        return render_template('result.html', result=result)
    return render_template('manual_entry.html')
@app.route('/all-students')
def all_students():
    if 'user' not in session:
        return redirect(url_for('login'))
    students = Student.query.filter_by(username=session['user']).all()
    return render_template('all_students.html', students=students)

from flask import jsonify
from collections import defaultdict

@app.route('/api/stats')
def stats_api():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    # Get all students for current user
    students = Student.query.filter_by(username=session['user']).all()
    dropout_details = DropoutStudentDetails.query.all()
    dropout_map = {d.student_id: d for d in dropout_details}

    # Gender stats (only for dropout students)
    gender_counts = defaultdict(int)
    state_counts = defaultdict(int)
    college_counts = defaultdict(int)
    age_counts = defaultdict(int)

    for student in students:
        # Only include dropout students in gender stats
        if student.status == 'dropout':
            gender = student.gender or 'Unknown'
            gender_counts[gender] += 1

        # State stats (from address)
        address = student.address or ''
        state = address.split(',')[-1].strip() if address else 'Unknown'
        state_counts[state] += 1

        # College stats
        college = student.clg_name or 'Unknown'
        college_counts[college] += 1

        # Age stats (from dob if available)
        if student.dob:
            from datetime import datetime
            try:
                dob = datetime.strptime(student.dob, '%Y-%m-%d')
                age = (datetime.now() - dob).days // 365
                age_group = f"{age//5*5}-{age//5*5+4}"
                age_counts[age_group] += 1
            except:
                age_counts['Unknown'] += 1

    return jsonify({
        'genderData': {
            'labels': list(gender_counts.keys()),
            'values': list(gender_counts.values())
        },
        'stateData': {
            'labels': list(state_counts.keys()),
            'values': list(state_counts.values())
        },
        'collegeData': {
            'labels': list(college_counts.keys()),
            'values': list(college_counts.values())
        },
        'ageData': {
            'labels': list(age_counts.keys()),
            'values': list(age_counts.values())
        }
    })

import logging

def calculate_dropout_percentage(marks_list, attendance_percent=0):
    """
    Calculate dropout percentage based on:
    Dropout % = ((1 - (avg_internal / 100)) * 0.3 + (1 - (avg_cgpa / 10)) * 0.5 + (1 - (attendance / 100)) * 0.2) * 100
    """

    internal_marks = []
    cgpas = []

    for mark in marks_list:
        # Collect internal marks from all known fields
        for key in mark:
            if key.startswith("internal") and isinstance(mark[key], (int, float)):
                internal_marks.append(mark[key])

        # Collect CGPA
        cgpa = mark.get("cgpa")
        if cgpa is not None:
            cgpas.append(cgpa)

    avg_internal = sum(internal_marks) / len(internal_marks) if internal_marks else 0
    avg_cgpa = sum(cgpas) / len(cgpas) if cgpas else 0

    dropout_percentage = (
        (1 - (avg_internal / 100)) * 0.3 +
        (1 - (avg_cgpa / 10)) * 0.5 +
        (1 - (attendance_percent / 100)) * 0.2
    ) * 100

    dropout_percentage = max(0, min(dropout_percentage, 100))  # Clamp between 0 and 100

    logging.debug(
        f"Dropout Calculation → avg_internal: {avg_internal}, avg_cgpa: {avg_cgpa}, "
        f"attendance: {attendance_percent}, dropout: {dropout_percentage:.2f}%"
    )

    return round(dropout_percentage, 2)


from flask import jsonify
import logging

from flask import jsonify
import logging

@app.route('/student-marks/<int:student_id>')
def student_marks(student_id):
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        logging.debug(f"Fetching marks for student_id: {student_id}, user: {session.get('user')}")
        # Verify the student belongs to the logged-in user
        student = Student.query.filter_by(id=student_id, username=session['user']).first()
        if not student:
            logging.debug(f"Student not found: {student_id} for user {session.get('user')}")
            return jsonify({'error': 'Student not found'}), 404
        marks = UniversityMarks.query.filter_by(student_id=student_id).all()
        logging.debug(f"Found {len(marks)} marks records for student {student_id}")
        marks_list = []
        for mark in marks:
            internal1_marks = mark.get_internal_marks(1)
            internal2_marks = mark.get_internal_marks(2)
            internal3_marks = mark.get_internal_marks(3)
            marks_list.append({
                'semester': mark.semester,
                'internal1_sub1': internal1_marks[0] if len(internal1_marks) > 0 else None,
                'internal1_sub2': internal1_marks[1] if len(internal1_marks) > 1 else None,
                'internal1_sub3': internal1_marks[2] if len(internal1_marks) > 2 else None,
                'internal1_sub4': internal1_marks[3] if len(internal1_marks) > 3 else None,
                'internal1_sub5': internal1_marks[4] if len(internal1_marks) > 4 else None,
                'internal1_sub6': internal1_marks[5] if len(internal1_marks) > 5 else None,
                'internal2_sub1': internal2_marks[0] if len(internal2_marks) > 0 else None,
                'internal2_sub2': internal2_marks[1] if len(internal2_marks) > 1 else None,
                'internal2_sub3': internal2_marks[2] if len(internal2_marks) > 2 else None,
                'internal2_sub4': internal2_marks[3] if len(internal2_marks) > 3 else None,
                'internal2_sub5': internal2_marks[4] if len(internal2_marks) > 4 else None,
                'internal2_sub6': internal2_marks[5] if len(internal2_marks) > 5 else None,
                'internal3_sub1': internal3_marks[0] if len(internal3_marks) > 0 else None,
                'internal3_sub2': internal3_marks[1] if len(internal3_marks) > 1 else None,
                'internal3_sub3': internal3_marks[2] if len(internal3_marks) > 2 else None,
                'internal3_sub4': internal3_marks[3] if len(internal3_marks) > 3 else None,
                'internal3_sub5': internal3_marks[4] if len(internal3_marks) > 4 else None,
                'internal3_sub6': internal3_marks[5] if len(internal3_marks) > 5 else None,
                'cgpa': mark.cgpa
            })
        attendance_percent = getattr(student, 'attendance_percent', 0) or 0
        dropout_percentage = calculate_dropout_percentage(marks_list, attendance_percent)
        return jsonify({'marks': marks_list, 'dropout_percentage': dropout_percentage})
    except Exception as e:
        logging.error(f"Error fetching marks for student {student_id}: {e}")
        return jsonify({'error': 'Error fetching marks.'}), 500

@app.route('/logout')
def logout():
    if 'user' in session:
        # Reset chat history before logging out
        return '''
        <script>
            if (typeof chatbase !== 'undefined' && typeof chatbase.reset === 'function') {
                chatbase.reset();
            }
            window.location.href = "/login";
        </script>
        '''
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/signout')
def signout():
    session.pop('user', None)
    flash('You have been successfully signed out.')
    return redirect(url_for('login'))
# ...existing code...

import requests
import xml.etree.ElementTree as ET
from flask import jsonify

@app.route('/api/news')
def api_news():
    rss_url = "https://news.google.com/rss/search?q=student+dropout&hl=en-US&gl=US&ceid=US:en"
    try:
        response = requests.get(rss_url)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        news_items = []
        # Google News RSS feed uses the 'item' tag for news entries
        for item in root.findall('.//item')[:10]:
            title = item.find('title').text if item.find('title') is not None else ''
            link = item.find('link').text if item.find('link') is not None else ''
            pubDate = item.find('pubDate').text if item.find('pubDate') is not None else ''

            # Try to extract image URL from media:content or media:thumbnail
            image_url = None
            media_content = item.find('{http://search.yahoo.com/mrss/}content')
            media_thumbnail = item.find('{http://search.yahoo.com/mrss/}thumbnail')
            if media_content is not None and 'url' in media_content.attrib:
                image_url = media_content.attrib['url']
            elif media_thumbnail is not None and 'url' in media_thumbnail.attrib:
                image_url = media_thumbnail.attrib['url']
            else:
                # Try to extract image from description HTML
                description = item.find('description').text if item.find('description') is not None else ''
                import re
                img_match = re.search(r'<img[^>]+src="([^">]+)"', description)
                if img_match:
                    image_url = img_match.group(1)

            if not image_url:
                image_url = "https://via.placeholder.com/250x140?text=No+Image"

            news_items.append({
                'title': title,
                'url': link,
                'date': pubDate,
                'image': image_url
            })
        return jsonify(news_items)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch news', 'details': str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.mkdir('uploads')
    with app.app_context():
        db.create_all() 
        app.run(debug=True) 