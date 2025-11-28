# Student Management System - Python + SQLite MVP

A basic/MVP version of the Student Management System using **only native Python and SQLite** - no web frameworks, no Flask, no frontend.

## 🎯 Purpose

This is a simplified version that demonstrates:
- Database creation and initialization
- CRUD operations (Create, Read, Update, Delete)
- SQL query execution with parameterized queries (SQL injection prevention)
- Simple command-line interface
- Pure Python with no external dependencies (except Python 3 standard library)

## 📁 Project Structure

```
python+sqlite branch/
├── init_db.py          # Database initialization script
├── student_manager.py  # Interactive CLI for CRUD operations
├── database.db         # SQLite database (created after init)
└── README_MVP.md       # This file
```

## 🚀 Setup & Usage

### Step 1: Initialize the Database

```bash
python3 init_db.py
```

This creates `database.db` with the following sample students:
- Alice Johnson (Grade: 92)
- Bob Smith (Grade: 78)
- Charlie Brown (Grade: 85)
- Diana Prince (Grade: 95)
- Eve Adams (Grade: 88)

### Step 2: Run the Student Manager

```bash
python3 student_manager.py
```

### Interactive Menu

```
--- MENU ---
1. View all students
2. View statistics
3. Search student by ID
4. Filter by minimum grade
5. Add new student
6. Update student
7. Delete student
8. Exit
```

## 📊 Database Schema

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    grade INTEGER CHECK(grade >= 0 AND grade <= 100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 💡 Example Usage

### View All Students
```bash
$ python3 student_manager.py
# Choose option 1

======================================================================
ID    Name                 Email                     Grade
======================================================================
1     Alice Johnson        alice@school.edu          92
2     Bob Smith            bob@school.edu            78
3     Charlie Brown        charlie@school.edu        85
4     Diana Prince         diana@school.edu          95
5     Eve Adams            eve@school.edu            88
======================================================================
```

### View Statistics
```bash
# Choose option 2

==================================================
GRADE STATISTICS
==================================================
Total Students: 5
Average Grade: 87.60
Highest Grade: 95
Lowest Grade: 78

Grade Distribution:
  A (90-100): 2
  B (80-89):  2
  C (70-79):  1
  Below 70:   0
==================================================
```

### Add New Student
```bash
# Choose option 5
Enter student name: John Doe
Enter student email: john@school.edu
Enter grade (0-100): 88

✓ Student added successfully with ID: 6
```

### Filter by Grade
```bash
# Choose option 4
Enter minimum grade (0-100): 90

======================================================================
ID    Name                 Email                     Grade
======================================================================
4     Diana Prince         diana@school.edu          95
1     Alice Johnson        alice@school.edu          92
======================================================================
```

## 🔧 Direct Python API Usage

You can also import and use the functions directly in your own Python scripts:

```python
from student_manager import (
    get_all_students,
    add_student,
    update_student,
    delete_student,
    get_statistics,
    filter_students_by_grade
)

# Get all students
students = get_all_students()
for student in students:
    print(f"{student['name']}: {student['grade']}")

# Add a student
student_id = add_student("Jane Smith", "jane@school.edu", 95)
print(f"Added student with ID: {student_id}")

# Get statistics
stats = get_statistics()
print(f"Average grade: {stats['average_grade']:.2f}")

# Filter high achievers
high_achievers = filter_students_by_grade(90)
print(f"Found {len(high_achievers)} students with grades >= 90")
```

## 📚 Key Features

### ✅ Implemented
- ✓ Database initialization with sample data
- ✓ View all students in table format
- ✓ Search student by ID
- ✓ Filter students by minimum grade
- ✓ Add new students with validation
- ✓ Update existing students
- ✓ Delete students with confirmation
- ✓ Real-time grade statistics
- ✓ Grade distribution analysis
- ✓ SQL injection prevention (parameterized queries)
- ✓ Input validation (grade range 0-100)
- ✓ Error handling for database operations

### 🔒 Security Features
- **Parameterized Queries**: All SQL uses `?` placeholders to prevent SQL injection
- **Input Validation**: Grade range validation (0-100)
- **Unique Email Constraint**: Database-level constraint prevents duplicate emails
- **Context Managers**: Proper database connection handling with automatic cleanup

## 🎓 Teaching Points

### 1. SQL Injection Prevention
```python
# ❌ WRONG - Vulnerable to SQL injection
cursor.execute(f"SELECT * FROM students WHERE id = {student_id}")

# ✓ CORRECT - Safe parameterized query
cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
```

### 2. Context Managers
```python
# Automatically closes connection, even if errors occur
with closing(connect_db()) as conn:
    cursor = conn.execute('SELECT * FROM students')
    return cursor.fetchall()
```

### 3. KISS Principle
- No external dependencies (pure Python 3)
- Simple, readable functions
- Clear separation of concerns
- Direct database access without ORM complexity

## 🛠️ Useful Commands

### Reset Database
```bash
rm database.db
python3 init_db.py
```

### View Database Directly
```bash
# Using SQLite CLI
sqlite3 database.db "SELECT * FROM students;"
sqlite3 database.db ".schema students"
```

### Make Scripts Executable
```bash
chmod +x init_db.py student_manager.py
./init_db.py
./student_manager.py
```

## 🔄 Differences from Full Version

| Feature | MVP (python+sqlite) | Full Version (main) |
|---------|-------------------|---------------------|
| Backend | Native Python | Flask REST API |
| Frontend | CLI only | HTML/CSS/JavaScript |
| Architecture | Single script | Client-Server |
| Dependencies | Python 3 stdlib | Flask, Flask-CORS |
| Interface | Terminal | Web Browser |
| Complexity | Simple | Moderate |

## 🚧 Limitations

- No web interface
- Single-user (no concurrent access handling)
- Terminal-based only
- No authentication/authorization
- Basic error messages
- No data export features

## 📈 Extension Ideas

1. **Export to CSV**: Add function to export student data
2. **Import from CSV**: Bulk import students from file
3. **Advanced Search**: Search by name or email patterns
4. **Grade History**: Track grade changes over time
5. **Backup/Restore**: Database backup functionality
6. **Sorting Options**: Sort by different fields
7. **Pagination**: Handle large student lists

## 🎯 Use Cases

This MVP is perfect for:
- Learning SQL and database operations
- Teaching Python database programming
- Understanding CRUD operations
- Command-line tool development
- Automated scripts and batch processing
- Testing and development without web overhead

## 🆚 When to Use Which Version

**Use MVP (python+sqlite)** when:
- Learning database basics
- Building automation scripts
- Developing backend-only tools
- Testing database logic
- No web interface needed

**Use Full Version (main branch)** when:
- Need web interface
- Multiple users access required
- Building production application
- Learning full-stack development
- API integration needed

## 📖 References

- [Python SQLite3 Documentation](https://docs.python.org/3/library/sqlite3.html)
- [SQLite SQL Syntax](https://www.sqlite.org/lang.html)
- [Context Managers in Python](https://docs.python.org/3/library/contextlib.html)

## 🏆 License

Educational project - Free to use and modify for learning purposes.

---

**Branch:** `python+sqlite`
**Type:** MVP / Basic Version
**Dependencies:** Python 3 (standard library only)
