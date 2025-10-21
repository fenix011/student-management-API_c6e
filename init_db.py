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
