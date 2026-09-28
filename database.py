import sqlite3
import hashlib
from datetime import date, timedelta
from pathlib import Path


# ==============================
# DATABASE LOCATION
# ==============================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "library.db"


# ==============================
# DATABASE CONNECTION
# ==============================

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


# ==============================
# PASSWORD HASHING
# ==============================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ==============================
# CREATE DATABASE TABLES
# ==============================

def init_database():

    connection = get_connection()
    cursor = connection.cursor()

    # Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            enrollment_no TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            course TEXT,
            semester TEXT,
            profile_photo BLOB,
            created_at TEXT NOT NULL
        )
    """)

    # Books table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT,
            isbn TEXT,
            total_copies INTEGER DEFAULT 1,
            available_copies INTEGER DEFAULT 1
        )
    """)

    # Issued books table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issued_books (
            issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            issue_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT,
            status TEXT DEFAULT 'Issued',
            fine REAL DEFAULT 0,

            FOREIGN KEY (student_id)
                REFERENCES students(student_id),

            FOREIGN KEY (book_id)
                REFERENCES books(book_id)
        )
    """)

    connection.commit()

    # Add sample books only if database has no books
    cursor.execute("SELECT COUNT(*) FROM books")
    book_count = cursor.fetchone()[0]

    if book_count == 0:

        books = [
            (
                "Python Programming",
                "Mark Lutz",
                "Programming",
                "978-9355423120",
                5,
                5
            ),
            (
                "Clean Code",
                "Robert C. Martin",
                "Programming",
                "978-0132350884",
                4,
                4
            ),
            (
                "Computer Networks",
                "Andrew S. Tanenbaum",
                "Computer Science",
                "978-0132126953",
                3,
                3
            ),
            (
                "Database System Concepts",
                "Abraham Silberschatz",
                "Database",
                "978-0078022159",
                4,
                4
            ),
            (
                "Artificial Intelligence",
                "Stuart Russell",
                "AI",
                "978-0134610993",
                3,
                3
            ),
            (
                "Data Science from Scratch",
                "Joel Grus",
                "Data Science",
                "978-1492041139",
                3,
                3
            ),
            (
                "Machine Learning with Python",
                "Sebastian Raschka",
                "Machine Learning",
                "978-1789955750",
                3,
                3
            ),
            (
                "Operating System Concepts",
                "Abraham Silberschatz",
                "Operating System",
                "978-1119800361",
                4,
                4
            )
        ]

        cursor.executemany("""
            INSERT INTO books
            (
                title,
                author,
                category,
                isbn,
                total_copies,
                available_copies
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, books)

        connection.commit()

    connection.close()


# ==============================
# CREATE STUDENT ACCOUNT
# ==============================

def create_student(
    name,
    enrollment_no,
    email,
    password,
    course,
    semester,
    profile_photo=None
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        hashed_password = hash_password(password)

        cursor.execute("""
            INSERT INTO students
            (
                name,
                enrollment_no,
                email,
                password,
                course,
                semester,
                profile_photo,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            enrollment_no,
            email,
            hashed_password,
            course,
            semester,
            profile_photo,
            str(date.today())
        ))

        connection.commit()

        student_id = cursor.lastrowid

        return True, student_id, "Account created successfully!"

    except sqlite3.IntegrityError:

        return False, None, "Email or Enrollment Number already exists."

    finally:

        connection.close()


# ==============================
# STUDENT LOGIN
# ==============================

def authenticate_student(email, password):

    connection = get_connection()
    cursor = connection.cursor()

    hashed_password = hash_password(password)

    cursor.execute("""
        SELECT *
        FROM students
        WHERE email = ?
        AND password = ?
    """, (
        email,
        hashed_password
    ))

    student = cursor.fetchone()

    connection.close()

    if student:
        return dict(student)

    return None


# ==============================
# GET STUDENT
# ==============================

def get_student(student_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM students
        WHERE student_id = ?
    """, (student_id,))

    student = cursor.fetchone()

    connection.close()

    if student:
        return dict(student)

    return None


# ==============================
# UPDATE STUDENT PROFILE
# ==============================

def update_profile(
    student_id,
    name,
    course,
    semester,
    profile_photo=None
):

    connection = get_connection()
    cursor = connection.cursor()

    if profile_photo is not None:

        cursor.execute("""
            UPDATE students
            SET name = ?,
                course = ?,
                semester = ?,
                profile_photo = ?
            WHERE student_id = ?
        """, (
            name,
            course,
            semester,
            profile_photo,
            student_id
        ))

    else:

        cursor.execute("""
            UPDATE students
            SET name = ?,
                course = ?,
                semester = ?
            WHERE student_id = ?
        """, (
            name,
            course,
            semester,
            student_id
        ))

    connection.commit()
    connection.close()


# ==============================
# GET ALL BOOKS
# ==============================

def get_all_books():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM books
        ORDER BY title
    """)

    books = cursor.fetchall()

    connection.close()

    return [dict(book) for book in books]


# ==============================
# GET SINGLE BOOK
# ==============================

def get_book(book_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM books
        WHERE book_id = ?
    """, (book_id,))

    book = cursor.fetchone()

    connection.close()

    if book:
        return dict(book)

    return None


# ==============================
# GET CATEGORIES
# ==============================

def get_categories():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT DISTINCT category
        FROM books
        WHERE category IS NOT NULL
        ORDER BY category
    """)

    categories = cursor.fetchall()

    connection.close()

    return [row["category"] for row in categories]


# ==============================
# ISSUE BOOK
# ==============================

def issue_book(student_id, book_id):

    connection = get_connection()
    cursor = connection.cursor()

    # Check available copies
    cursor.execute("""
        SELECT available_copies
        FROM books
        WHERE book_id = ?
    """, (book_id,))

    book = cursor.fetchone()

    if not book:
        connection.close()
        return False, "Book not found."

    if book["available_copies"] <= 0:
        connection.close()
        return False, "This book is currently unavailable."

    # Check if student already has this book
    cursor.execute("""
        SELECT issue_id
        FROM issued_books
        WHERE student_id = ?
        AND book_id = ?
        AND status = 'Issued'
    """, (
        student_id,
        book_id
    ))

    existing = cursor.fetchone()

    if existing:
        connection.close()
        return False, "You already have this book issued."

    issue_date = date.today()
    due_date = issue_date + timedelta(days=10)

    # Add issue record
    cursor.execute("""
        INSERT INTO issued_books
        (
            student_id,
            book_id,
            issue_date,
            due_date,
            status,
            fine
        )
        VALUES (?, ?, ?, ?, 'Issued', 0)
    """, (
        student_id,
        book_id,
        str(issue_date),
        str(due_date)
    ))

    # Decrease available copy
    cursor.execute("""
        UPDATE books
        SET available_copies = available_copies - 1
        WHERE book_id = ?
    """, (book_id,))

    connection.commit()
    connection.close()

    return True, f"Book issued successfully. Due date: {due_date}"


# ==============================
# GET STUDENT BOOKS
# ==============================

def get_student_books(student_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            issued_books.*,
            books.title,
            books.author,
            books.category
        FROM issued_books

        JOIN books
        ON issued_books.book_id = books.book_id

        WHERE issued_books.student_id = ?

        ORDER BY issued_books.issue_id DESC
    """, (student_id,))

    books = cursor.fetchall()

    connection.close()

    return [dict(book) for book in books]


# ==============================
# RETURN BOOK
# ==============================

def return_book(issue_id, student_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM issued_books
        WHERE issue_id = ?
        AND student_id = ?
        AND status = 'Issued'
    """, (
        issue_id,
        student_id
    ))

    issue = cursor.fetchone()

    if not issue:
        connection.close()
        return False, "Issue record not found."

    return_date = date.today()

    due_date = date.fromisoformat(issue["due_date"])

    late_days = max(
        0,
        (return_date - due_date).days
    )

    # ₹5 fine per late day
    fine = late_days * 5

    cursor.execute("""
        UPDATE issued_books
        SET return_date = ?,
            status = 'Returned',
            fine = ?
        WHERE issue_id = ?
    """, (
        str(return_date),
        fine,
        issue_id
    ))

    # Increase available copy
    cursor.execute("""
        UPDATE books
        SET available_copies = available_copies + 1
        WHERE book_id = ?
    """, (issue["book_id"],))

    connection.commit()
    connection.close()

    return True, f"Book returned successfully. Fine: ₹{fine}"


# ==============================
# STUDENT STATISTICS
# ==============================

def get_student_statistics(student_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM issued_books
        WHERE student_id = ?
    """, (student_id,))

    total_issues = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM issued_books
        WHERE student_id = ?
        AND status = 'Issued'
    """, (student_id,))

    active_books = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM issued_books
        WHERE student_id = ?
        AND status = 'Returned'
    """, (student_id,))

    returned_books = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(fine), 0)
        FROM issued_books
        WHERE student_id = ?
    """, (student_id,))

    total_fine = cursor.fetchone()[0]

    connection.close()

    return {
        "total_issues": total_issues,
        "active_books": active_books,
        "returned_books": returned_books,
        "total_fine": total_fine
    }  