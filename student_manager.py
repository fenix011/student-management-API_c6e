#!/usr/bin/env python3
"""
Simple Student Management System - MVP
Uses native Python + SQLite (no Flask, no web interface)
"""
import sqlite3
from contextlib import closing


def connect_db():
    """Create a database connection"""
    return sqlite3.connect('database.db')


def get_all_students():
    """Retrieve all students from the database"""
    with closing(connect_db()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute('SELECT * FROM students ORDER BY name')
        return [dict(row) for row in cursor.fetchall()]


def get_student_by_id(student_id):
    """Get a specific student by ID"""
    with closing(connect_db()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def add_student(name, email, grade):
    """Add a new student to the database"""
    if not (0 <= grade <= 100):
        raise ValueError("Grade must be between 0 and 100")

    with closing(connect_db()) as conn:
        cursor = conn.execute(
            'INSERT INTO students (name, email, grade) VALUES (?, ?, ?)',
            (name, email, grade)
        )
        conn.commit()
        return cursor.lastrowid


def update_student(student_id, name, email, grade):
    """Update an existing student"""
    if not (0 <= grade <= 100):
        raise ValueError("Grade must be between 0 and 100")

    with closing(connect_db()) as conn:
        cursor = conn.execute(
            'UPDATE students SET name = ?, email = ?, grade = ? WHERE id = ?',
            (name, email, grade, student_id)
        )
        conn.commit()
        return cursor.rowcount > 0


def delete_student(student_id):
    """Delete a student from the database"""
    with closing(connect_db()) as conn:
        cursor = conn.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        return cursor.rowcount > 0


def get_statistics():
    """Get grade statistics"""
    with closing(connect_db()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute('''
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
        ''')
        row = cursor.fetchone()
        return dict(row) if row else None


def filter_students_by_grade(min_grade):
    """Get students with grade >= min_grade"""
    with closing(connect_db()) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            'SELECT * FROM students WHERE grade >= ? ORDER BY grade DESC',
            (min_grade,)
        )
        return [dict(row) for row in cursor.fetchall()]


def print_student(student):
    """Pretty print a student record"""
    if not student:
        print("Student not found")
        return

    print(f"\nID: {student['id']}")
    print(f"Name: {student['name']}")
    print(f"Email: {student['email']}")
    print(f"Grade: {student['grade']}")
    print(f"Created: {student['created_at']}")


def print_students_table(students):
    """Print students in a table format"""
    if not students:
        print("\nNo students found.")
        return

    print("\n" + "="*70)
    print(f"{'ID':<5} {'Name':<20} {'Email':<25} {'Grade':<5}")
    print("="*70)
    for student in students:
        print(f"{student['id']:<5} {student['name']:<20} {student['email']:<25} {student['grade']:<5}")
    print("="*70)


def print_statistics(stats):
    """Pretty print statistics"""
    if not stats:
        print("No statistics available")
        return

    print("\n" + "="*50)
    print("GRADE STATISTICS")
    print("="*50)
    print(f"Total Students: {stats['total_students']}")
    print(f"Average Grade: {stats['average_grade']:.2f}" if stats['average_grade'] else "Average Grade: N/A")
    print(f"Highest Grade: {stats['highest_grade']}")
    print(f"Lowest Grade: {stats['lowest_grade']}")
    print("\nGrade Distribution:")
    print(f"  A (90-100): {stats['a_students']}")
    print(f"  B (80-89):  {stats['b_students']}")
    print(f"  C (70-79):  {stats['c_students']}")
    print(f"  Below 70:   {stats['failing_students']}")
    print("="*50)


def main():
    """Interactive CLI for student management"""
    print("\n" + "="*50)
    print("STUDENT MANAGEMENT SYSTEM - MVP")
    print("Native Python + SQLite")
    print("="*50)

    while True:
        print("\n--- MENU ---")
        print("1. View all students")
        print("2. View statistics")
        print("3. Search student by ID")
        print("4. Filter by minimum grade")
        print("5. Add new student")
        print("6. Update student")
        print("7. Delete student")
        print("8. Exit")

        choice = input("\nEnter your choice (1-8): ").strip()

        try:
            if choice == '1':
                students = get_all_students()
                print_students_table(students)

            elif choice == '2':
                stats = get_statistics()
                print_statistics(stats)

            elif choice == '3':
                student_id = int(input("Enter student ID: "))
                student = get_student_by_id(student_id)
                print_student(student)

            elif choice == '4':
                min_grade = int(input("Enter minimum grade (0-100): "))
                students = filter_students_by_grade(min_grade)
                print_students_table(students)

            elif choice == '5':
                name = input("Enter student name: ").strip()
                email = input("Enter student email: ").strip()
                grade = int(input("Enter grade (0-100): "))
                student_id = add_student(name, email, grade)
                print(f"\n✓ Student added successfully with ID: {student_id}")

            elif choice == '6':
                student_id = int(input("Enter student ID to update: "))
                student = get_student_by_id(student_id)
                if not student:
                    print("Student not found!")
                    continue

                print_student(student)
                name = input(f"Enter new name [{student['name']}]: ").strip() or student['name']
                email = input(f"Enter new email [{student['email']}]: ").strip() or student['email']
                grade_input = input(f"Enter new grade [{student['grade']}]: ").strip()
                grade = int(grade_input) if grade_input else student['grade']

                if update_student(student_id, name, email, grade):
                    print("\n✓ Student updated successfully")
                else:
                    print("\n✗ Failed to update student")

            elif choice == '7':
                student_id = int(input("Enter student ID to delete: "))
                confirm = input(f"Are you sure you want to delete student {student_id}? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    if delete_student(student_id):
                        print("\n✓ Student deleted successfully")
                    else:
                        print("\n✗ Student not found")
                else:
                    print("Delete cancelled")

            elif choice == '8':
                print("\nGoodbye!")
                break

            else:
                print("\n✗ Invalid choice. Please try again.")

        except ValueError as e:
            print(f"\n✗ Error: {e}")
        except sqlite3.IntegrityError as e:
            print(f"\n✗ Database error: {e}")
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")


if __name__ == '__main__':
    # Check if database exists
    try:
        with closing(connect_db()) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM students")
            count = cursor.fetchone()[0]
            print(f"Database found with {count} students")
    except sqlite3.OperationalError:
        print("Database not found! Please run: python3 init_db.py")
        exit(1)

    main()
