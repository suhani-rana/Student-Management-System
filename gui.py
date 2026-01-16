import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
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

# Functions
def add_student():
    roll = roll_entry.get()
    name = name_entry.get()
    course = course_entry.get()
    sem = sem_entry.get()

    if roll == "" or name == "" or course == "" or sem == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        cursor.execute("INSERT INTO students (roll_no, name, course, semester) VALUES (?, ?, ?, ?)",
                       (roll, name, course, sem))
        conn.commit()
        messagebox.showinfo("Success", "Student Added Successfully!")
        clear_fields()
        view_students()
    except:
        messagebox.showerror("Error", "Roll No already exists!")

def view_students():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT roll_no, name, course, semester FROM students")
    rows = cursor.fetchall()

    for row in rows:
        listbox.insert(tk.END, row)

def search_student():
    roll = roll_entry.get()
    if roll == "":
        messagebox.showerror("Error", "Enter Roll No to search!")
        return

    cursor.execute("SELECT roll_no, name, course, semester FROM students WHERE roll_no=?", (roll,))
    row = cursor.fetchone()

    listbox.delete(0, tk.END)
    if row:
        listbox.insert(tk.END, row)
    else:
        messagebox.showinfo("Not Found", "Student not found!")

def update_student():
    roll = roll_entry.get()
    name = name_entry.get()
    course = course_entry.get()
    sem = sem_entry.get()

    if roll == "":
        messagebox.showerror("Error", "Roll No is required to update!")
        return

    cursor.execute("SELECT * FROM students WHERE roll_no=?", (roll,))
    student = cursor.fetchone()

    if not student:
        messagebox.showinfo("Not Found", "Student not found!")
        return

    cursor.execute("""
    UPDATE students SET name=?, course=?, semester=? WHERE roll_no=?
    """, (name, course, sem, roll))
    conn.commit()
    messagebox.showinfo("Success", "Student Updated Successfully!")
    clear_fields()
    view_students()

def delete_student():
    roll = roll_entry.get()
    if roll == "":
        messagebox.showerror("Error", "Enter Roll No to delete!")
        return

    cursor.execute("SELECT * FROM students WHERE roll_no=?", (roll,))
    student = cursor.fetchone()

    if not student:
        messagebox.showinfo("Not Found", "Student not found!")
        return

    cursor.execute("DELETE FROM students WHERE roll_no=?", (roll,))
    conn.commit()
    messagebox.showinfo("Success", "Student Deleted Successfully!")
    clear_fields()
    view_students()

def clear_fields():
    roll_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    sem_entry.delete(0, tk.END)

# GUI Window
root = tk.Tk()
root.title("Student Management System (GUI)")
root.geometry("700x450")

# Labels + Entries
tk.Label(root, text="Roll No").place(x=20, y=20)
roll_entry = tk.Entry(root, width=25)
roll_entry.place(x=100, y=20)

tk.Label(root, text="Name").place(x=20, y=60)
name_entry = tk.Entry(root, width=25)
name_entry.place(x=100, y=60)

tk.Label(root, text="Course").place(x=20, y=100)
course_entry = tk.Entry(root, width=25)
course_entry.place(x=100, y=100)

tk.Label(root, text="Semester").place(x=20, y=140)
sem_entry = tk.Entry(root, width=25)
sem_entry.place(x=100, y=140)

# Buttons
tk.Button(root, text="Add", width=12, command=add_student).place(x=20, y=190)
tk.Button(root, text="View All", width=12, command=view_students).place(x=130, y=190)
tk.Button(root, text="Search", width=12, command=search_student).place(x=240, y=190)
tk.Button(root, text="Update", width=12, command=update_student).place(x=350, y=190)
tk.Button(root, text="Delete", width=12, command=delete_student).place(x=460, y=190)
tk.Button(root, text="Clear", width=12, command=clear_fields).place(x=570, y=190)

# Listbox
listbox = tk.Listbox(root, width=90, height=12)
listbox.place(x=20, y=240)

view_students()
root.mainloop()