import tkinter as tk
from tkinter import messagebox
import json, os

students = {}
DATA_FILE = "students.json"

# ================= FILE =================
def load_students():
    global students
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            students = json.load(f)

def save_students():
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=4)

# ================= CLEAR =================
def clear_add():
    for e in [name_entry, prog_entry, src_entry, e1, e2, e3, e4]:
        e.delete(0, tk.END)
    avg_var.set("")
    remarks_var.set("")

def clear_search():
    search_entry.delete(0, tk.END)
    result_name.set("")
    result_program.set("")
    result_avg.set("")
    result_remarks.set("")

def clear_delete():
    del_sr.delete(0, tk.END)
    del_name.delete(0, tk.END)
    del_prog.delete(0, tk.END)

def clear_update():
    update_sr_entry.delete(0, tk.END)
    update_name_entry.delete(0, tk.END)
    update_program_entry.delete(0, tk.END)
    for e in update_courses:
        e.delete(0, tk.END)

# ================= ADD =================
def compute():
    try:
        grades = [float(e1.get()), float(e2.get()), float(e3.get()), float(e4.get())]
        avg = sum(grades) / 4
        avg_var.set(f"{avg:.2f}")
        remarks = "PASS" if avg <= 3.00 else "FAIL"

        sr = src_entry.get()

        if sr in students:
           messagebox.showerror("Error", "SR-Code already exists!")
           clear_add()         
           name_entry.focus()   
           return

        students[sr] = {
            "name": name_entry.get(),
            "program": prog_entry.get(),
            "grades": dict(zip(["Integral","Pathfit","ACP","Discrete"], grades)),
            "average": avg,
            "remarks": remarks
        }

        save_students()
        messagebox.showinfo("Success", "Student saved!")
        clear_add()

        

    except ValueError:
        messagebox.showerror("Error", "Invalid input!")

# ================= SEARCH =================
def search_student():
    sr = search_entry.get()

    if sr in students:
        d = students[sr]
        result_name.set(d["name"])
        result_program.set(d["program"])
        result_avg.set(f"{d['average']:.2f}")
        result_remarks.set(d["remarks"])
    else:
        messagebox.showerror("Not Found", "Student not found!")

# ================= UPDATE =================
def load_update_data():
    sr = update_sr_entry.get()
    if sr in students:
        d = students[sr]

        update_name_entry.delete(0, tk.END)
        update_program_entry.delete(0, tk.END)

        update_name_entry.insert(0, d["name"])
        update_program_entry.insert(0, d["program"])

        for i, sub in enumerate(["Integral","Pathfit","ACP","Discrete"]):
            update_courses[i].delete(0, tk.END)
            update_courses[i].insert(0, d["grades"][sub])
    else:
        messagebox.showerror("Error", "Student not found!")

def update_student_full():
    try:
        sr = update_sr_entry.get()
        if sr not in students:
            messagebox.showerror("Error", "Student not found!")
            return

        grades = [float(e.get()) for e in update_courses]
        avg = sum(grades)/4
        remarks = "FAIL" if avg >= 3 else "PASS"

        students[sr] = {
            "name": update_name_entry.get(),
            "program": update_program_entry.get(),
            "grades": dict(zip(["Integral","Pathfit","ACP","Discrete"], grades)),
            "average": avg,
            "remarks": remarks
        }

        save_students()
        messagebox.showinfo("Success", "Student updated!")
        clear_update()

    except ValueError:
        messagebox.showerror("Error", "Invalid grades!")

# ================= DELETE =================
def delete_search():
    sr = del_sr.get()

    del_name.delete(0, tk.END)
    del_prog.delete(0, tk.END)

    if sr in students:
        d = students[sr]
        del_name.insert(0, d["name"])
        del_prog.insert(0, d["program"])
    else:
        messagebox.showerror("Error", "Student not found!")
        clear_delete()

def confirm_window():
    win = tk.Toplevel(root)
    win.title("Confirm Delete")
    win.geometry("250x150")

    tk.Label(win, text="Delete this student?").pack(pady=15)

    center_frame = tk.Frame(win)
    center_frame.pack(expand=True)

    btn_frame = tk.Frame(center_frame)
    btn_frame.pack(expand=True)

    def yes():
        sr = del_sr.get()
        if sr in students:
            students.pop(sr)
            save_students()
            messagebox.showinfo("Deleted", "Student deleted!")
            clear_delete()
        win.destroy()

    tk.Button(btn_frame, text="YES", bg="red", fg="white", width=8, command=yes).pack(side="left", padx=10)
    tk.Button(btn_frame, text="NO", width=8, command=win.destroy).pack(side="left", padx=10)

# ================= VIEW =================
def refresh_table():
    for row in entries:
        for cell in row:
            cell.delete(0, tk.END)

    for i, (sr, data) in enumerate(students.items()):
        if i >= len(entries): break
        entries[i][0].insert(0, data["name"])
        entries[i][1].insert(0, sr)
        entries[i][2].insert(0, data["program"])
        entries[i][3].insert(0, f"{data['average']:.2f}")
        entries[i][4].insert(0, data["remarks"])

def show_records():
    hide_all()
    page_title.config(text="VIEW RECORDS")
    view_frame.pack(padx=20, pady=20)
    refresh_table()

# ================= SWITCH =================
def show_add():
    hide_all()
    page_title.config(text="ADD STUDENT")
    add_frame.pack(padx=50, pady=20)

def show_search():
    hide_all()
    page_title.config(text="SEARCH STUDENT")
    search_frame.pack(padx=50, pady=20)

def show_update():
    hide_all()
    page_title.config(text="UPDATE STUDENT")
    update_frame.pack(padx=50, pady=20)

def show_delete():
    hide_all()
    page_title.config(text="DELETE STUDENT")
    delete_frame.pack(padx=50, pady=20)

def hide_all():
    add_frame.pack_forget()
    search_frame.pack_forget()
    update_frame.pack_forget()
    delete_frame.pack_forget()
    view_frame.pack_forget()

# ================= UI =================
root = tk.Tk()
root.title("Enhanced Student Record System")
root.geometry("1000x600")
root.configure(bg="white")

# HEADER
header = tk.Frame(root, bg="white", height=60)
header.pack(side="top", fill="x")

title_frame = tk.Frame(header, bg="white")
title_frame.pack(fill="x", padx=20, pady=5)

page_title = tk.Label(title_frame, text="ADD STUDENT",
                      font=("Arial",14,"bold"), bg="white", fg="black")
page_title.pack(side="left")

tk.Label(title_frame, text="Enhanced Student Record System",
         font=("Arial",18,"bold"), bg="white").pack()

# SIDEBAR
sidebar = tk.Frame(root, bg="black", width=180)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(sidebar, text="MENU", bg="black", fg="white",
         font=("Arial",12,"bold")).pack(pady=(15,10))

tk.Button(sidebar, text="Add Student", width=15, command=show_add).pack(pady=5)
tk.Button(sidebar, text="Search", width=15, command=show_search).pack(pady=5)
tk.Button(sidebar, text="Update", width=15, command=show_update).pack(pady=5)
tk.Button(sidebar, text="Delete", width=15, command=show_delete).pack(pady=5)
tk.Button(sidebar, text="View Records", width=15, command=show_records).pack(pady=5)

# ================= ADD =================
add_frame = tk.Frame(root, bg="white")

tk.Label(add_frame, text="Name").grid(row=1,column=0)
tk.Label(add_frame, text="Program").grid(row=2,column=0)
tk.Label(add_frame, text="SR-Code").grid(row=3,column=0)

name_entry = tk.Entry(add_frame); name_entry.grid(row=1, column=1)
prog_entry = tk.Entry(add_frame); prog_entry.grid(row=2, column=1)
src_entry = tk.Entry(add_frame); src_entry.grid(row=3, column=1)

tk.Label(add_frame,text="Integral").grid(row=5,column=0)
tk.Label(add_frame,text="Pathfit").grid(row=5,column=2)
tk.Label(add_frame,text="ACP").grid(row=6,column=0)
tk.Label(add_frame,text="Discrete").grid(row=6,column=2)

e1 = tk.Entry(add_frame); e1.grid(row=5, column=1)
e2 = tk.Entry(add_frame); e2.grid(row=5, column=3)
e3 = tk.Entry(add_frame); e3.grid(row=6, column=1)
e4 = tk.Entry(add_frame); e4.grid(row=6, column=3)

avg_var = tk.StringVar()
remarks_var = tk.StringVar()

tk.Label(add_frame, text="Average").grid(row=8,column=0)
tk.Label(add_frame, text="Remarks").grid(row=8,column=2)

tk.Entry(add_frame,textvariable=avg_var).grid(row=8,column=1)
tk.Entry(add_frame,textvariable=remarks_var).grid(row=8,column=3)

tk.Button(add_frame,text="ENTER",command=compute).grid(row=1,column=3)

# ================= SEARCH =================
search_frame = tk.Frame(root, bg="white")

tk.Label(search_frame, text="SR Code:").grid(row=0,column=0)

search_entry = tk.Entry(search_frame)
search_entry.grid(row=0,column=1)

tk.Button(search_frame,text="SEARCH",command=search_student).grid(row=0,column=2)
tk.Button(search_frame,text="CLEAR",command=clear_search).grid(row=0,column=3)

tk.Label(search_frame, text="Name:").grid(row=1,column=0)
tk.Label(search_frame, text="Program:").grid(row=1,column=1)
tk.Label(search_frame, text="Average:").grid(row=2,column=0)
tk.Label(search_frame, text="Remarks:").grid(row=2,column=1)

result_name = tk.StringVar()
result_program = tk.StringVar()
result_avg = tk.StringVar()
result_remarks = tk.StringVar()

tk.Entry(search_frame,textvariable=result_name).grid(row=1,column=0)
tk.Entry(search_frame,textvariable=result_program).grid(row=1,column=1)
tk.Entry(search_frame,textvariable=result_avg).grid(row=2,column=0)
tk.Entry(search_frame,textvariable=result_remarks).grid(row=2,column=1)

# ================= UPDATE =================
update_frame = tk.Frame(root, bg="white")

tk.Label(update_frame, text="SR Code:").grid(row=0,column=0)

update_sr_entry = tk.Entry(update_frame)
update_sr_entry.grid(row=0,column=1)

tk.Button(update_frame,text="ENTER",command=load_update_data).grid(row=0,column=2)

tk.Label(update_frame, text="Name:").grid(row=1,column=0)
tk.Label(update_frame, text="Program:").grid(row=2,column=0)

update_name_entry = tk.Entry(update_frame)
update_program_entry = tk.Entry(update_frame)

update_name_entry.grid(row=1,column=1)
update_program_entry.grid(row=2,column=1)

update_courses = []
for i, sub in enumerate(["Integral","Pathfit","ACP","Discrete"]):
    tk.Label(update_frame,text=sub).grid(row=3+i,column=0)
    e = tk.Entry(update_frame)
    e.grid(row=3+i,column=1)
    update_courses.append(e)

tk.Button(update_frame,text="Update",command=update_student_full).grid(row=8,column=1)

# ================= DELETE =================
delete_frame = tk.Frame(root, bg="white")

tk.Label(delete_frame, text="SR-Code:").grid(row=0,column=0)

del_sr = tk.Entry(delete_frame)
del_sr.grid(row=0,column=1)

tk.Button(delete_frame,text="Search",command=delete_search).grid(row=0,column=2)
tk.Button(delete_frame,text="Delete",command=confirm_window).grid(row=3,column=1)

tk.Label(delete_frame, text="Name:").grid(row=1,column=0)
tk.Label(delete_frame, text="Program:").grid(row=2,column=0)

del_name = tk.Entry(delete_frame)
del_prog = tk.Entry(delete_frame)

del_name.grid(row=1,column=1)
del_prog.grid(row=2,column=1)

# ================= VIEW =================
view_frame = tk.Frame(root, bg="white")

headers = ["Name","SR-Code","Program","Average","Pass/Fail"]

for col,h in enumerate(headers):
    tk.Label(view_frame,text=h,bg="white",bd=1,relief="solid",width=18)\
        .grid(row=0,column=col,padx=5,pady=5)

entries = []
for r in range(1,17):
    row=[]
    for c in range(5):
        e=tk.Entry(view_frame,width=20,bd=1,relief="solid")
        e.grid(row=r,column=c,padx=5,pady=5)
        row.append(e)
    entries.append(row)

# ================= START =================
load_students()
show_add()
root.mainloop()