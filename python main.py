import sqlite3

# Database connection
conn = sqlite3.connect("student.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    course TEXT NOT NULL,
    semester INTEGER NOT NULL
)
""")
conn.commit()


def add_student():
    roll_no = input("Enter Roll No: ")
    name = input("Enter Name: ")
    course = input("Enter Course: ")
    semester = input("Enter Semester: ")

    try:
        cursor.execute(
            "INSERT INTO students (roll_no, name, course, semester) VALUES (?, ?, ?, ?)",
            (roll_no, name, course, semester)
        )
        conn.commit()
        print("✅ Student Added Successfully!")
    except:
        print("❌ Roll No already exists! Try a different one.")


def view_students():
    cursor.execute("SELECT roll_no, name, course, semester FROM students")
    students = cursor.fetchall()

    print("\n--- Student List ---")
    if len(students) == 0:
        print("No students found.")
    else:
        for s in students:
            print(s)


def search_student():
    roll_no = input("Enter Roll No to Search: ")

    cursor.execute("SELECT roll_no, name, course, semester FROM students WHERE roll_no = ?", (roll_no,))
    student = cursor.fetchone()

    if student:
        print("✅ Student Found:", student)
    else:
        print("❌ Student not found!")


def update_student():
    roll_no = input("Enter Roll No to Update: ")

    cursor.execute("SELECT * FROM students WHERE roll_no = ?", (roll_no,))
    student = cursor.fetchone()

    if not student:
        print("❌ Student not found!")
        return

    new_name = input("Enter New Name: ")
    new_course = input("Enter New Course: ")
    new_semester = input("Enter New Semester: ")

    cursor.execute("""
    UPDATE students
    SET name = ?, course = ?, semester = ?
    WHERE roll_no = ?
    """, (new_name, new_course, new_semester, roll_no))

    conn.commit()
    print("✅ Student Updated Successfully!")


def delete_student():
    roll_no = input("Enter Roll No to Delete: ")

    cursor.execute("SELECT * FROM students WHERE roll_no = ?", (roll_no,))
    student = cursor.fetchone()

    if not student:
        print("❌ Student not found!")
        return

    cursor.execute("DELETE FROM students WHERE roll_no = ?", (roll_no,))
    conn.commit()
    print("✅ Student Deleted Successfully!")


while True:
    print("\n===== Student Management System =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()
    elif choice == "2":
        view_students()
    elif choice == "3":
        search_student()
    elif choice == "4":
        update_student()
    elif choice == "5":
        delete_student()
    elif choice == "6":
        print("Bye 👋")
        break
    else:
        print("❌ Invalid choice! Try again.")