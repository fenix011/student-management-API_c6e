# Student Management API

A complete full-stack teaching example demonstrating client-server architecture, RESTful API design, and functional programming principles using vanilla JavaScript and Flask.

## Overview

This project demonstrates:
- **Backend:** Python Flask REST API with SQLite database
- **Frontend:** Vanilla JavaScript (ES6+) with functional programming patterns
- **Architecture:** Clean separation of concerns following KISS principle
- **Security:** SQL injection prevention via parameterized queries
- **Design Pattern:** Revealing Module Pattern for JavaScript organization

## Project Structure

```
student-management-API_c6e/
├── backend.py          # Flask API server (RESTful endpoints)
├── init_db.py          # Database initialization script
├── database.db         # SQLite database (created after init)
├── index.html          # Frontend interface
├── app.js             # Vanilla JavaScript (functional approach)
├── style.css          # Minimal CSS styling
├── CLAUDE.md          # Complete teaching documentation
└── README.md          # This file
```

## Features

- **CRUD Operations:** Create, Read, Update, Delete students
- **Real-time Statistics:** Average grades, distribution, min/max
- **Grade Filtering:** Filter students by minimum grade
- **Grade Categories:** Color-coded grades (A/B/C/Failing)
- **Form Validation:** Client and server-side validation
- **Error Handling:** Proper HTTP status codes and user feedback
- **Responsive Design:** Clean, modern interface

## Technologies

- **Backend:** Python 3, Flask, Flask-CORS, SQLite3
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6+)
- **API:** RESTful architecture with JSON
- **Database:** SQLite with parameterized queries

## Setup Instructions

### Prerequisites

- Python 3.x installed
- pip (Python package manager)
- Modern web browser

### 1. Install Python Dependencies

```bash
pip install flask flask-cors
```

### 2. Initialize the Database

```bash
python3 init_db.py
```

This creates `database.db` and populates it with 5 sample students:
- Alice Johnson (92)
- Bob Smith (78)
- Charlie Brown (85)
- Diana Prince (95)
- Eve Adams (88)

### 3. Start the Backend Server

```bash
python3 backend.py
```

The Flask API server will start on `http://127.0.0.1:5000`

You should see:
```
 * Serving Flask app 'backend'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### 4. Open the Frontend

**IMPORTANT:** You need to run a separate HTTP server for the frontend!

**Option A: Serve with Python HTTP server (recommended)**
```bash
# In a NEW terminal window (keep backend running in the first)
python3 -m http.server 8000
```
Then open your browser to: `http://localhost:8000`

**Option B: Open directly**
```bash
xdg-open index.html
# or simply open index.html in your browser
```
Note: This may cause CORS issues with some browsers.

## ⚠️ Common Error: 404 When Accessing Backend Directly

**WRONG:** Opening `http://127.0.0.1:5000` in your browser
- **Result:** 404 Error - "The requested URL was not found on the server"
- **Why:** The Flask backend is an API-only server with no HTML routes

**CORRECT:** This is a TWO-SERVER architecture:

1. **Backend API Server (Port 5000)** - Serves JSON data only
   ```
   Terminal 1: python3 backend.py
   Routes: /api/students, /api/statistics, etc.
   DO NOT access http://localhost:5000 in browser!
   ```

2. **Frontend HTTP Server (Port 8000)** - Serves HTML/CSS/JS files
   ```
   Terminal 2: python3 -m http.server 8000
   Access: http://localhost:8000 ← Use this URL!
   ```

**How it works:**
```
Browser → localhost:8000 → index.html loads
                             ↓
                        app.js makes fetch() calls
                             ↓
                        localhost:5000/api/*
                             ↓
                        Flask returns JSON
```

**Testing the API directly (for development):**
```bash
# Use curl, not your browser
curl http://localhost:5000/api/students
curl http://localhost:5000/api/statistics
```

## Usage

### Web Interface

1. **View Students:** The main page displays all students with their grades
2. **Add Student:** Click "Add Student" button, fill the form, submit
3. **Edit Student:** Click "Edit" on any student card
4. **Delete Student:** Click "Delete" (with confirmation)
5. **Filter by Grade:** Use the "Min Grade" input to filter students
6. **View Statistics:** See real-time grade statistics at the top

### API Endpoints

Base URL: `http://localhost:5000/api`

#### Get All Students
```bash
GET /api/students
curl http://localhost:5000/api/students
```

#### Filter Students by Grade
```bash
GET /api/students?min_grade=90
curl http://localhost:5000/api/students?min_grade=90
```

#### Get Single Student
```bash
GET /api/students/<id>
curl http://localhost:5000/api/students/1
```

#### Create Student
```bash
POST /api/students
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@school.edu","grade":87}'
```

#### Update Student
```bash
PUT /api/students/<id>
curl -X PUT http://localhost:5000/api/students/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice Johnson","email":"alice@school.edu","grade":95}'
```

#### Delete Student
```bash
DELETE /api/students/<id>
curl -X DELETE http://localhost:5000/api/students/1
```

#### Get Statistics
```bash
GET /api/statistics
curl http://localhost:5000/api/statistics
```

Response example:
```json
{
  "total_students": 5,
  "average_grade": 87.6,
  "highest_grade": 95,
  "lowest_grade": 78,
  "a_students": 2,
  "b_students": 2,
  "c_students": 1,
  "failing_students": 0
}
```

## Database Schema

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    grade INTEGER CHECK(grade >= 0 AND grade <= 100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Teaching Points

### Security Concepts
1. **SQL Injection Prevention:** Parameterized queries (`?` placeholders)
2. **Input Validation:** Server-side validation before database operations
3. **CORS Handling:** Controlled cross-origin requests
4. **Error Handling:** Proper HTTP status codes (400, 404, 201)

### Functional Programming
1. **Pure Functions:** API helper functions without side effects
2. **Higher-Order Functions:** `validate_json` decorator pattern
3. **Function Composition:** Building complex operations from simple functions
4. **Immutability:** Not modifying data directly

### KISS Principles
1. **Single Responsibility:** Each function does one thing
2. **Minimal Dependencies:** Only Flask and built-in libraries
3. **Clear Naming:** Self-documenting code
4. **No Over-Engineering:** SQLite instead of complex ORMs

### Design Patterns
1. **Revealing Module Pattern:** JavaScript app organization
2. **Decorator Pattern:** Input validation in Flask
3. **MVC-like Separation:** Routes, data layer, presentation separate

## Troubleshooting

### 404 Error - "URL not found on the server"
**Symptom:** Opening http://127.0.0.1:5000 shows 404 error

**Cause:** You're accessing the API backend directly. It only serves JSON at /api/* routes.

**Solution:**
1. Keep backend running (Terminal 1: `python3 backend.py`)
2. Start frontend server (Terminal 2: `python3 -m http.server 8000`)
3. Open browser to `http://localhost:8000` (NOT port 5000!)

See the "⚠️ Common Error" section above for full details.

### Port 5000 Already in Use
```bash
# Find and kill the process using port 5000
lsof -i :5000
kill -9 <PID>

# Or use a different port in backend.py
app.run(debug=True, port=5001)
```

### CORS Errors
Make sure Flask-CORS is installed and the backend is running. The `CORS(app)` line in backend.py enables cross-origin requests.

### Database Locked
If you get "database is locked" errors:
```bash
rm database.db
python3 init_db.py
```

### Frontend Not Loading Data
1. Check backend is running: `curl http://localhost:5000/api/students`
2. Check browser console for errors (F12)
3. Verify API_BASE URL in app.js matches your backend

## Development Tips

### Reset Database
```bash
rm database.db
python3 init_db.py
```

### View Database Contents
```bash
sqlite3 database.db "SELECT * FROM students;"
```

### Enable/Disable Debug Mode
In `backend.py`, change:
```python
app.run(debug=True, port=5000)  # Development
app.run(debug=False, port=5000)  # Production-like
```

## Exercise Ideas for Students

1. **Add Search:** Implement name/email search functionality
2. **Pagination:** Handle large student lists with pages
3. **Export CSV:** Add endpoint to export data as CSV
4. **Authentication:** Implement simple token-based auth
5. **Sorting:** Add sorting by name, grade, date
6. **Bulk Operations:** Delete or update multiple students
7. **Grade History:** Track grade changes over time
8. **Input Sanitization:** Add additional validation rules

## References

- [MDN Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [MDN async/await](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQL Injection Prevention](https://developer.mozilla.org/en-US/docs/Glossary/SQL_Injection)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

## License

Educational project - Free to use and modify for teaching purposes.

## Author

Teaching example following KISS principle and Unix philosophy.
Created for Computer Science education.

---

**Current Status:**
- Backend API Server: Running on http://127.0.0.1:5000
- Database: Initialized with 5 sample students
- Ready to use!
