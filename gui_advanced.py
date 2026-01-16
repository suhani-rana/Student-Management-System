import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------------- Database Setup ----------------
conn = sqlite3.connect("student.db")
cursor = conn.cursor()

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

# ---------------- Validation ----------------
def is_valid_name(name):
    return name.replace(" ", "").isalpha()

def is_valid_semester(sem):
    return sem.isdigit() and 1 <= int(sem) <= 6

# ---------------- Treeview Functions ----------------
def clear_table():
    for item in tree.get_children():
        tree.delete(item)

def load_students():
    clear_table()
    cursor.execute("SELECT roll_no, name, course, semester FROM students ORDER BY name ASC")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

def on_tree_select(event):
    selected = tree.focus()
    if selected == "":
        return

    values = tree.item(selected, "values")
    if not values:
        return

    roll_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    sem_entry.delete(0, tk.END)

    roll_entry.insert(0, values[0])
    name_entry.insert(0, values[1])
    course_entry.insert(0, values[2])
    sem_entry.insert(0, values[3])

# ---------------- CRUD Functions ----------------
def add_student():
    roll = roll_entry.get().strip()
    name = name_entry.get().strip()
    course = course_entry.get().strip()
    sem = sem_entry.get().strip()

    if roll == "" or name == "" or course == "" or sem == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    if not is_valid_name(name):
        messagebox.showerror("Error", "Name should contain only alphabets!")
        return

    if not is_valid_semester(sem):
        messagebox.showerror("Error", "Semester must be between 1 to 6!")
        return

    try:
        cursor.execute(
            "INSERT INTO students (roll_no, name, course, semester) VALUES (?, ?, ?, ?)",
            (roll, name, course, int(sem))
        )
        conn.commit()
        messagebox.showinfo("Success", "Student Added Successfully!")
        clear_fields()
        load_students()
    except:
        messagebox.showerror("Error", "Roll No already exists!")

def update_student():
    roll = roll_entry.get().strip()
    name = name_entry.get().strip()
    course = course_entry.get().strip()
    sem = sem_entry.get().strip()

    if roll == "":
        messagebox.showerror("Error", "Roll No is required to update!")
        return

    cursor.execute("SELECT * FROM students WHERE roll_no=?", (roll,))
    student = cursor.fetchone()

    if not student:
        messagebox.showinfo("Not Found", "Student not found!")
        return

    if name == "" or course == "" or sem == "":
        messagebox.showerror("Error", "Fill all fields before updating!")
        return

    if not is_valid_name(name):
        messagebox.showerror("Error", "Name should contain only alphabets!")
        return

    if not is_valid_semester(sem):
        messagebox.showerror("Error", "Semester must be between 1 to 6!")
        return

    cursor.execute("""
        UPDATE students
        SET name=?, course=?, semester=?
        WHERE roll_no=?
    """, (name, course, int(sem), roll))

    conn.commit()
    messagebox.showinfo("Success", "Student Updated Successfully!")
    clear_fields()
    load_students()

def delete_student():
    roll = roll_entry.get().strip()

    if roll == "":
        messagebox.showerror("Error", "Enter Roll No to delete!")
        return

    cursor.execute("SELECT * FROM students WHERE roll_no=?", (roll,))
    student = cursor.fetchone()

    if not student:
        messagebox.showinfo("Not Found", "Student not found!")
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?")
    if confirm:
        cursor.execute("DELETE FROM students WHERE roll_no=?", (roll,))
        conn.commit()
        messagebox.showinfo("Success", "Student Deleted Successfully!")
        clear_fields()
        load_students()

def clear_fields():
    roll_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    sem_entry.delete(0, tk.END)

# ---------------- Search Functions ----------------
def search_students():
    keyword = search_entry.get().strip()

    if keyword == "":
        messagebox.showerror("Error", "Enter Roll No or Name to search!")
        return

    clear_table()

    cursor.execute("""
        SELECT roll_no, name, course, semester
        FROM students
        WHERE roll_no LIKE ? OR name LIKE ?
        ORDER BY name ASC
    """, (f"%{keyword}%", f"%{keyword}%"))

    rows = cursor.fetchall()

    if not rows:
        messagebox.showinfo("Not Found", "No matching student found!")
        return

    for row in rows:
        tree.insert("", tk.END, values=row)

def show_all():
    search_entry.delete(0, tk.END)
    load_students()

# ---------------- GUI Window ----------------
root = tk.Tk()
root.title("Student Management System (Advanced GUI)")
root.geometry("880x560")
root.resizable(False, False)

title = tk.Label(root, text="Student Management System", font=("Arial", 18, "bold"))
title.pack(pady=10)

# ---------------- Form Frame ----------------
frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="Roll No").grid(row=0, column=0, padx=10, pady=8, sticky="w")
roll_entry = tk.Entry(frame, width=25)
roll_entry.grid(row=0, column=1, padx=10, pady=8)

tk.Label(frame, text="Name").grid(row=0, column=2, padx=10, pady=8, sticky="w")
name_entry = tk.Entry(frame, width=25)
name_entry.grid(row=0, column=3, padx=10, pady=8)

tk.Label(frame, text="Course").grid(row=1, column=0, padx=10, pady=8, sticky="w")
course_entry = tk.Entry(frame, width=25)
course_entry.grid(row=1, column=1, padx=10, pady=8)

tk.Label(frame, text="Semester").grid(row=1, column=2, padx=10, pady=8, sticky="w")
sem_entry = tk.Entry(frame, width=25)
sem_entry.grid(row=1, column=3, padx=10, pady=8)

# ---------------- Buttons Frame ----------------
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Student", width=15, command=add_student).grid(row=0, column=0, padx=8)
tk.Button(btn_frame, text="Update", width=15, command=update_student).grid(row=0, column=1, padx=8)
tk.Button(btn_frame, text="Delete", width=15, command=delete_student).grid(row=0, column=2, padx=8)
tk.Button(btn_frame, text="Clear", width=15, command=clear_fields).grid(row=0, column=3, padx=8)

# ---------------- Search Frame ----------------
search_frame = tk.Frame(root)
search_frame.pack(pady=5)

tk.Label(search_frame, text="Search (Roll/Name):").grid(row=0, column=0, padx=8)
search_entry = tk.Entry(search_frame, width=30)
search_entry.grid(row=0, column=1, padx=8)

tk.Button(search_frame, text="Search", width=12, command=search_students).grid(row=0, column=2, padx=8)
tk.Button(search_frame, text="Show All", width=12, command=show_all).grid(row=0, column=3, padx=8)

# ---------------- Treeview Table ----------------
columns = ("roll_no", "name", "course", "semester")
tree = ttk.Treeview(root, columns=columns, show="headings", height=13)

tree.heading("roll_no", text="Roll No")
tree.heading("name", text="Name")
tree.heading("course", text="Course")
tree.heading("semester", text="Semester")

tree.column("roll_no", width=120)
tree.column("name", width=240)
tree.column("course", width=240)
tree.column("semester", width=120)

tree.pack(pady=10)

tree.bind("<<TreeviewSelect>>", on_tree_select)

load_students()
root.mainloop()