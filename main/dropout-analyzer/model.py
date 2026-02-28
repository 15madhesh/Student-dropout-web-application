def analyze_dropout(data, manual=False):
    if manual:
        # Use all fields from manual entry
        result = {
            'stud_name': data.get('stud_name'),
            'dob': data.get('dob'),
            'status': data.get('status'),
            'sslc_marks': data.get('sslc_marks'),
            'hsc_marks': data.get('hsc_marks'),
            'clg_name': data.get('clg_name'),
            'mother_name': data.get('mother_name'),
            'father_name': data.get('father_name'),
            'address': data.get('address'),
        }
        # Example dropout logic using marks and status
        try:
            sslc = float(data.get('sslc_marks', 0))
            hsc = float(data.get('hsc_marks', 0))
            dropout_rate = (1 - (sslc / 100)) * (1 - (hsc / 100))
        except Exception:
            dropout_rate = None
        result['dropout_rate'] = dropout_rate
        return result
    else:
        # Parse all student entries from CSV
        import csv
        results = []
        with open(data, 'r', encoding='latin1') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    name = row.get('name', '')
                    age = float(row.get('age', 0))
                    attendance = float(row.get('attendance', 0))
                    marks = float(row.get('marks', 0))
                    dropout_rate = (1 - (attendance / 100)) * (1 - (marks / 100))
                    results.append({
                        'name': name,
                        'age': age,
                        'attendance': attendance,
                        'marks': marks,
                        'dropout_rate': dropout_rate
                    })
                except ValueError:
                    continue
        return results if results else {
            'error': 'Invalid CSV format. Ensure columns: name,age,attendance,marks',
            'students': []
        }
        return {
            'age': age,
            'attendance': attendance,
            'marks': marks,
            'dropout_rate': dropout_rate
        }