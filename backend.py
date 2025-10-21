#!/usr/bin/env python3
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import sqlite3
from contextlib import closing
from functools import wraps

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests for teaching purposes

# Database helper function (functional approach)
def query_db(query, args=(), one=False):
    """Execute a query and return results as dictionaries"""
    with closing(sqlite3.connect('database.db')) as conn:
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = conn.execute(query, args)
        rows = cursor.fetchall()
        return (rows[0] if rows else None) if one else rows

def dict_from_row(row):
    """Convert sqlite3.Row to dictionary"""
    return dict(row) if row else None

# Input validation decorator (functional programming style)
def validate_json(*required_fields):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request.json:
                abort(400, description="No JSON data provided")
            for field in required_fields:
                if field not in request.json:
                    abort(400, description=f"Missing required field: {field}")
            return f(*args, **kwargs)
        return wrapper
    return decorator

# --- API ROUTES ---

@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all students or filter by grade"""
    min_grade = request.args.get('min_grade', type=int)

    if min_grade is not None:
        students = query_db(
            'SELECT * FROM students WHERE grade >= ? ORDER BY grade DESC',
            [min_grade]
        )
    else:
        students = query_db('SELECT * FROM students ORDER BY name')

    return jsonify([dict_from_row(s) for s in students])

@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Get a specific student by ID"""
    student = query_db(
        'SELECT * FROM students WHERE id = ?',
        [student_id],
        one=True
    )

    if not student:
        abort(404, description="Student not found")

    return jsonify(dict_from_row(student))

@app.route('/api/students', methods=['POST'])
@validate_json('name', 'email', 'grade')
def create_student():
    """Create a new student"""
    data = request.json

    # Validate grade range
    if not 0 <= data['grade'] <= 100:
        abort(400, description="Grade must be between 0 and 100")

    try:
        with closing(sqlite3.connect('database.db')) as conn:
            cursor = conn.execute(
                'INSERT INTO students (name, email, grade) VALUES (?, ?, ?)',
                [data['name'], data['email'], data['grade']]
            )
            conn.commit()
            student_id = cursor.lastrowid

        # Return the created student
        return jsonify({
            'id': student_id,
            'message': 'Student created successfully'
        }), 201

    except sqlite3.IntegrityError as e:
        abort(400, description="Email already exists")

@app.route('/api/students/<int:student_id>', methods=['PUT'])
@validate_json('name', 'email', 'grade')
def update_student(student_id):
    """Update an existing student"""
    data = request.json

    # Check if student exists
    if not query_db('SELECT id FROM students WHERE id = ?', [student_id], one=True):
        abort(404, description="Student not found")

    with closing(sqlite3.connect('database.db')) as conn:
        conn.execute(
            'UPDATE students SET name = ?, email = ?, grade = ? WHERE id = ?',
            [data['name'], data['email'], data['grade'], student_id]
        )
        conn.commit()

    return jsonify({'message': 'Student updated successfully'})

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete a student"""
    with closing(sqlite3.connect('database.db')) as conn:
        cursor = conn.execute('DELETE FROM students WHERE id = ?', [student_id])
        conn.commit()

        if cursor.rowcount == 0:
            abort(404, description="Student not found")

    return jsonify({'message': 'Student deleted successfully'})

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get grade statistics (functional approach with SQL aggregation)"""
    stats = query_db('''
        SELECT
            COUNT(*) as total_students,
            AVG(grade) as average_grade,
            MAX(grade) as highest_grade,
            MIN(grade) as lowest_grade,
            COUNT(CASE WHEN grade >= 90 THEN 1 END) as a_students,
            COUNT(CASE WHEN grade >= 80 AND grade < 90 THEN 1 END) as b_students,
            COUNT(CASE WHEN grade >= 70 AND grade < 80 THEN 1 END) as c_students,
            COUNT(CASE WHEN grade < 70 THEN 1 END) as failing_students
        FROM students
    ''', one=True)

    return jsonify(dict_from_row(stats))

# Error handlers
@app.errorhandler(400)
@app.errorhandler(404)
def handle_error(error):
    return jsonify({
        'error': error.description,
        'status': error.code
    }), error.code

if __name__ == '__main__':
    app.run(debug=True, port=5000)
