# Student Management API - Complete Teaching Example

## Project Structure
```
student-management/
├── backend.py          # Flask API server
├── database.db         # SQLite database
├── index.html          # Frontend interface
├── app.js             # Vanilla JavaScript
├── style.css          # Simple styling
└── init_db.py         # Database setup script
```

## 1. Database Setup (`init_db.py`)

```python
#!/usr/bin/env python3
import sqlite3

# Following KISS: Simple schema, clear purpose
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create students table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        grade INTEGER CHECK(grade >= 0 AND grade <= 100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Insert sample data
sample_students = [
    ('Alice Johnson', 'alice@school.edu', 92),
    ('Bob Smith', 'bob@school.edu', 78),
    ('Charlie Brown', 'charlie@school.edu', 85),
    ('Diana Prince', 'diana@school.edu', 95),
    ('Eve Adams', 'eve@school.edu', 88)
]

cursor.executemany(
    'INSERT OR IGNORE INTO students (name, email, grade) VALUES (?, ?, ?)',
    sample_students
)

conn.commit()
conn.close()
print("Database initialized with sample data")
```

## 2. Backend API (`backend.py`)

```python
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
```

## 3. Frontend HTML (`index.html`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Management System</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>Student Management System</h1>
        <p>Demonstrating Client-Server Architecture</p>
    </header>

    <main>
        <!-- Statistics Section -->
        <section id="statistics">
            <h2>Grade Statistics</h2>
            <div id="stats-container"></div>
        </section>

        <!-- Student List -->
        <section id="students">
            <h2>Students</h2>
            <div class="controls">
                <button onclick="StudentApp.loadStudents()">Refresh</button>
                <button onclick="StudentApp.showAddForm()">Add Student</button>
                <label>
                    Min Grade:
                    <input type="number" id="minGrade" min="0" max="100" 
                           onchange="StudentApp.filterByGrade(this.value)">
                </label>
            </div>
            <div id="student-list"></div>
        </section>

        <!-- Add/Edit Form (hidden by default) -->
        <section id="student-form" class="hidden">
            <h2 id="form-title">Add Student</h2>
            <form onsubmit="StudentApp.saveStudent(event)">
                <input type="hidden" id="studentId">
                <label>
                    Name:
                    <input type="text" id="studentName" required>
                </label>
                <label>
                    Email:
                    <input type="email" id="studentEmail" required>
                </label>
                <label>
                    Grade:
                    <input type="number" id="studentGrade" min="0" max="100" required>
                </label>
                <div class="form-buttons">
                    <button type="submit">Save</button>
                    <button type="button" onclick="StudentApp.hideForm()">Cancel</button>
                </div>
            </form>
        </section>
    </main>

    <footer>
        <p>Teaching Example - KISS Principle Applied</p>
    </footer>

    <script src="app.js"></script>
</body>
</html>
```

## 4. Vanilla JavaScript (`app.js`)

```javascript
// Functional programming approach with minimal state
const API_BASE = 'http://localhost:5000/api';

// Pure functions for API calls
const api = {
    async get(endpoint) {
        const response = await fetch(`${API_BASE}${endpoint}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
    },

    async post(endpoint, data) {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
    },

    async put(endpoint, data) {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
    },

    async delete(endpoint) {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
    }
};

// Student App Module (Revealing Module Pattern)
const StudentApp = (function() {
    
    // Private functions
    const renderStudent = (student) => `
        <div class="student-card">
            <h3>${student.name}</h3>
            <p>Email: ${student.email}</p>
            <p>Grade: <span class="grade ${getGradeClass(student.grade)}">${student.grade}</span></p>
            <div class="actions">
                <button onclick="StudentApp.editStudent(${student.id})">Edit</button>
                <button onclick="StudentApp.deleteStudent(${student.id})" class="danger">Delete</button>
            </div>
        </div>
    `;

    const getGradeClass = (grade) => {
        if (grade >= 90) return 'excellent';
        if (grade >= 80) return 'good';
        if (grade >= 70) return 'average';
        return 'poor';
    };

    const renderStatistics = (stats) => `
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Students</h3>
                <p class="stat-value">${stats.total_students}</p>
            </div>
            <div class="stat-card">
                <h3>Average Grade</h3>
                <p class="stat-value">${stats.average_grade?.toFixed(1) || 'N/A'}</p>
            </div>
            <div class="stat-card">
                <h3>Highest Grade</h3>
                <p class="stat-value">${stats.highest_grade || 'N/A'}</p>
            </div>
            <div class="stat-card">
                <h3>Lowest Grade</h3>
                <p class="stat-value">${stats.lowest_grade || 'N/A'}</p>
            </div>
            <div class="stat-card">
                <h3>Grade Distribution</h3>
                <ul>
                    <li>A (90-100): ${stats.a_students}</li>
                    <li>B (80-89): ${stats.b_students}</li>
                    <li>C (70-79): ${stats.c_students}</li>
                    <li>Below 70: ${stats.failing_students}</li>
                </ul>
            </div>
        </div>
    `;

    const showError = (message) => {
        alert(`Error: ${message}`);
    };

    // Public API
    return {
        async loadStudents() {
            try {
                const students = await api.get('/students');
                const container = document.getElementById('student-list');
                
                if (students.length === 0) {
                    container.innerHTML = '<p>No students found</p>';
                } else {
                    container.innerHTML = students.map(renderStudent).join('');
                }
                
                // Also load statistics
                this.loadStatistics();
            } catch (error) {
                showError('Failed to load students');
                console.error(error);
            }
        },

        async loadStatistics() {
            try {
                const stats = await api.get('/statistics');
                document.getElementById('stats-container').innerHTML = renderStatistics(stats);
            } catch (error) {
                console.error('Failed to load statistics:', error);
            }
        },

        async filterByGrade(minGrade) {
            try {
                const endpoint = minGrade ? `/students?min_grade=${minGrade}` : '/students';
                const students = await api.get(endpoint);
                const container = document.getElementById('student-list');
                
                if (students.length === 0) {
                    container.innerHTML = '<p>No students found with this filter</p>';
                } else {
                    container.innerHTML = students.map(renderStudent).join('');
                }
            } catch (error) {
                showError('Failed to filter students');
            }
        },

        showAddForm() {
            document.getElementById('form-title').textContent = 'Add Student';
            document.getElementById('studentId').value = '';
            document.getElementById('studentName').value = '';
            document.getElementById('studentEmail').value = '';
            document.getElementById('studentGrade').value = '';
            document.getElementById('student-form').classList.remove('hidden');
        },

        async editStudent(id) {
            try {
                const student = await api.get(`/students/${id}`);
                document.getElementById('form-title').textContent = 'Edit Student';
                document.getElementById('studentId').value = student.id;
                document.getElementById('studentName').value = student.name;
                document.getElementById('studentEmail').value = student.email;
                document.getElementById('studentGrade').value = student.grade;
                document.getElementById('student-form').classList.remove('hidden');
            } catch (error) {
                showError('Failed to load student data');
            }
        },

        hideForm() {
            document.getElementById('student-form').classList.add('hidden');
        },

        async saveStudent(event) {
            event.preventDefault();
            
            const id = document.getElementById('studentId').value;
            const data = {
                name: document.getElementById('studentName').value,
                email: document.getElementById('studentEmail').value,
                grade: parseInt(document.getElementById('studentGrade').value)
            };

            try {
                if (id) {
                    await api.put(`/students/${id}`, data);
                } else {
                    await api.post('/students', data);
                }
                
                this.hideForm();
                this.loadStudents();
            } catch (error) {
                showError('Failed to save student');
            }
        },

        async deleteStudent(id) {
            if (!confirm('Are you sure you want to delete this student?')) {
                return;
            }

            try {
                await api.delete(`/students/${id}`);
                this.loadStudents();
            } catch (error) {
                showError('Failed to delete student');
            }
        }
    };
})();

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    StudentApp.loadStudents();
});
```

## 5. Simple CSS (`style.css`)

```css
/* KISS: Minimal, functional CSS */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    line-height: 1.6;
    color: #333;
    background: #f4f4f4;
}

header {
    background: #2c3e50;
    color: white;
    text-align: center;
    padding: 1rem;
}

main {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1rem;
}

section {
    background: white;
    margin-bottom: 2rem;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

h2 {
    margin-bottom: 1rem;
    color: #2c3e50;
}

.controls {
    margin-bottom: 1rem;
    display: flex;
    gap: 1rem;
    align-items: center;
}

.student-card {
    border: 1px solid #ddd;
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 4px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.grade {
    font-weight: bold;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
}

.grade.excellent { background: #27ae60; color: white; }
.grade.good { background: #3498db; color: white; }
.grade.average { background: #f39c12; color: white; }
.grade.poor { background: #e74c3c; color: white; }

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
}

.stat-card {
    background: #ecf0f1;
    padding: 1rem;
    border-radius: 4px;
    text-align: center;
}

.stat-value {
    font-size: 2rem;
    font-weight: bold;
    color: #2c3e50;
}

button {
    background: #3498db;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background: #2980b9;
}

button.danger {
    background: #e74c3c;
}

button.danger:hover {
    background: #c0392b;
}

form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-width: 400px;
}

label {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

input {
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.form-buttons {
    display: flex;
    gap: 1rem;
}

.hidden {
    display: none;
}

footer {
    text-align: center;
    padding: 2rem;
    color: #7f8c8d;
}
```

## Running the Application

### 1. Install Dependencies
```bash
pip install flask flask-cors
```

### 2. Initialize Database
```bash
python init_db.py
```

### 3. Start the Backend Server
```bash
python backend.py
```

### 4. Open Frontend
Open `index.html` in your browser (or serve it with a simple HTTP server):
```bash
python -m http.server 8000
# Then navigate to http://localhost:8000
```

## Key Teaching Points

### Security Concepts Demonstrated
1. **SQL Injection Prevention**: Using parameterized queries (`?` placeholders)
2. **Input Validation**: Server-side validation before database operations
3. **CORS**: Understanding cross-origin requests
4. **Error Handling**: Proper HTTP status codes and error messages

### Functional Programming Concepts
1. **Pure Functions**: API helper functions with no side effects
2. **Higher-Order Functions**: `validate_json` decorator
3. **Immutability**: Not modifying data directly, creating new responses
4. **Function Composition**: Building complex operations from simple functions

### KISS Principles Applied
1. **Single Responsibility**: Each function does one thing
2. **Minimal Dependencies**: Only Flask and built-in libraries
3. **Clear Naming**: Functions and variables describe their purpose
4. **No Over-Engineering**: Simple SQLite instead of complex ORMs

### Unix Philosophy
1. **Modularity**: Separate files for different concerns
2. **Text Interfaces**: JSON API for communication
3. **Simplicity**: Each component can be understood independently
4. **Composition**: Frontend and backend work independently

## Exercise Ideas for Students

1. **Add Search Functionality**: Implement name/email search
2. **Pagination**: Handle large student lists
3. **Export Data**: Add CSV export endpoint
4. **Authentication**: Add simple token-based auth
5. **Real-time Updates**: Implement WebSocket notifications
6. **Testing**: Write unit tests for API endpoints

## Common Mistakes to Discuss

1. **Exposing SQL in Frontend**: Why we never send raw SQL from client
2. **Missing Validation**: Always validate on the server
3. **Synchronous Thinking**: Understanding async/await
4. **Global State**: Why we use module pattern instead

## References
- [MDN Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [MDN async/await](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQL Injection Prevention](https://developer.mozilla.org/en-US/docs/Glossary/SQL_Injection)