@app.route('/update_marks', methods=['GET', 'POST'])
def update_marks():
    if 'user_id' not in session:
        return redirect(url_for('signin'))

    students = Student.query.all()
    success = None

    if request.method == 'POST':
        student_id = request.form['student_id']
        semester = int(request.form['semester'])
        stage = request.form['stage']
        sub1 = float(request.form.get('sub1', 0))
        sub2 = float(request.form.get('sub2', 0))
        sub3 = float(request.form.get('sub3', 0))
        sub4 = float(request.form.get('sub4', 0))
        sub5 = float(request.form.get('sub5', 0))
        sub6 = float(request.form.get('sub6', 0))
        cgpa = request.form.get('cgpa')

        mark = UniversityMarks.query.filter_by(student_id=student_id, semester=semester).first()
        if not mark:
            mark = UniversityMarks(student_id=student_id, semester=semester)
            db.session.add(mark)

        if stage == 'internal1':
            mark.internal1_sub1 = sub1
            mark.internal1_sub2 = sub2
            mark.internal1_sub3 = sub3
            mark.internal1_sub4 = sub4
            mark.internal1_sub5 = sub5
            mark.internal1_sub6 = sub6
        elif stage == 'internal2':
            mark.internal2_sub1 = sub1
            mark.internal2_sub2 = sub2
            mark.internal2_sub3 = sub3
            mark.internal2_sub4 = sub4
            mark.internal2_sub5 = sub5
            mark.internal2_sub6 = sub6
        elif stage == 'internal3':
            mark.internal3_sub1 = sub1
            mark.internal3_sub2 = sub2
            mark.internal3_sub3 = sub3
            mark.internal3_sub4 = sub4
            mark.internal3_sub5 = sub5
            mark.internal3_sub6 = sub6
        elif stage == 'cgpa' and cgpa:
            mark.cgpa = float(cgpa)

        db.session.commit()
        success = "Marks updated successfully!"

    return render_template("update_marks.html", students=students, success=success)
