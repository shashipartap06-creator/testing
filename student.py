from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
from create_db import create_db

class studentClass:
    def __init__(self, root):
        self.root = root
        self.root.title("SRMS — Manage Students")
        self.root.geometry("1350x750+50+50")
        self.root.config(bg="#F0F4F8")
        self.root.focus_force()

        # Variables
        self.var_rollno = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_contact = StringVar()
        self.var_course = StringVar()
        self.var_admission = StringVar()
        self.var_state = StringVar()
        self.var_city = StringVar()
        self.var_pin = StringVar()
        self.var_search = StringVar()

        self.course_list = []
        self.entry_fields = []

        self._create_title_bar()
        self._build_layout()
        self.fetch_course()
        self.show()

    def _create_title_bar(self):
        title_bar = Frame(self.root, bg="#1A3E6F", height=50)
        title_bar.pack(fill=X, side=TOP)
        title_bar.pack_propagate(False)
        Label(title_bar, text="👨‍🎓  Manage Student Details",
              font=("Segoe UI", 18, "bold"), bg="#1A3E6F", fg="white").pack(side=LEFT, padx=20, pady=8)

    def _build_layout(self):
        main_frame = Frame(self.root, bg="#F0F4F8")
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=15)

        # ========== LEFT PANEL (Student Information) ==========
        left_container = LabelFrame(main_frame, text=" Student Information ",
                                    font=("Segoe UI", 12, "bold"),
                                    bg="white", fg="#1A3E6F", bd=2, relief=GROOVE)
        left_container.pack(side=LEFT, fill=BOTH, expand=False, padx=(0, 15), ipadx=5, ipady=5)
        left_container.config(width=500)  # fixed width
        left_container.pack_propagate(False)

        # Canvas + Scrollbar for scrollable form
        canvas = Canvas(left_container, bg="white", highlightthickness=0)
        scrollbar = Scrollbar(left_container, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="white")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=480)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Two-column layout inside scrollable_frame
        form_frame = scrollable_frame
        col1 = Frame(form_frame, bg="white")
        col1.grid(row=0, column=0, padx=15, pady=5, sticky="nsew")
        col2 = Frame(form_frame, bg="white")
        col2.grid(row=0, column=1, padx=15, pady=5, sticky="nsew")
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)

        # ----- Column 1 fields -----
        self._add_field(col1, "Roll No.", self.var_rollno, 0)
        self._add_field(col1, "Name", self.var_name, 2)
        self._add_field(col1, "Email", self.var_email, 4)
        self._add_combo(col1, "Gender", self.var_gender, 6, ("Select", "Male", "Female", "Other"))
        self._add_field(col1, "State", self.var_state, 8)
        self._add_field(col1, "City", self.var_city, 10)
        self._add_field(col1, "PIN Code", self.var_pin, 12)

        # ----- Column 2 fields -----
        self._add_field(col2, "Date of Birth", self.var_dob, 0)
        self._add_field(col2, "Contact", self.var_contact, 2)
        self._add_field(col2, "Admission Date", self.var_admission, 4)
        # Course combobox - store reference
        self.txt_course = self._add_combo(col2, "Course", self.var_course, 6, self.course_list, readonly=True)

        # Address field (spans both columns)
        addr_label = Label(form_frame, text="Address", font=("Segoe UI", 11, "bold"),
                           bg="white", fg="#333")
        addr_label.grid(row=14, column=0, columnspan=2, sticky="w", padx=15, pady=(15, 5))
        self.txt_address = Text(form_frame, font=("Segoe UI", 10), bg="#F0F4F8",
                                relief=SOLID, bd=1, height=5, width=55)
        self.txt_address.grid(row=15, column=0, columnspan=2, padx=15, pady=(0, 15), sticky="ew")
        self.txt_address.bind("<Return>", self._on_enter_text)

        # Buttons
        btn_frame = Frame(form_frame, bg="white")
        btn_frame.grid(row=16, column=0, columnspan=2, pady=(5, 15), sticky="ew")
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)
        btn_frame.grid_columnconfigure(3, weight=1)

        Button(btn_frame, text="💾 Save", font=("Segoe UI", 10, "bold"),
               bg="#27AE60", fg="white", cursor="hand2", relief=FLAT,
               command=self.add, padx=15, pady=5).grid(row=0, column=0, padx=5, sticky="ew")
        Button(btn_frame, text="✏️ Update", font=("Segoe UI", 10, "bold"),
               bg="#2B6CB0", fg="white", cursor="hand2", relief=FLAT,
               command=self.update, padx=15, pady=5).grid(row=0, column=1, padx=5, sticky="ew")
        Button(btn_frame, text="🗑 Delete", font=("Segoe UI", 10, "bold"),
               bg="#C0392B", fg="white", cursor="hand2", relief=FLAT,
               command=self.delete, padx=15, pady=5).grid(row=0, column=2, padx=5, sticky="ew")
        Button(btn_frame, text="✖ Clear", font=("Segoe UI", 10, "bold"),
               bg="#7F8C8D", fg="white", cursor="hand2", relief=FLAT,
               command=self.clear, padx=15, pady=5).grid(row=0, column=3, padx=5, sticky="ew")

        # ========== RIGHT PANEL (Search + Table) ==========
        right_panel = Frame(main_frame, bg="#F0F4F8")
        right_panel.pack(side=LEFT, fill=BOTH, expand=True)

        # Search Panel
        search_frame = LabelFrame(right_panel, text=" Search Student ",
                                  font=("Segoe UI", 11, "bold"),
                                  bg="white", fg="#1A3E6F", bd=2, relief=GROOVE)
        search_frame.pack(fill=X, pady=(0, 15), ipady=8)

        Label(search_frame, text="Roll No:", font=("Segoe UI", 10, "bold"),
              bg="white", fg="#333").pack(side=LEFT, padx=(15, 10))
        self.search_entry = Entry(search_frame, textvariable=self.var_search,
                                  font=("Segoe UI", 10), bg="#F0F4F8", relief=SOLID, bd=1, width=20)
        self.search_entry.pack(side=LEFT, padx=5)
        self.search_entry.bind("<Return>", lambda e: self.search())
        Button(search_frame, text="🔍 Search", font=("Segoe UI", 10, "bold"),
               bg="#2B6CB0", fg="white", cursor="hand2", relief=FLAT,
               command=self.search, padx=15, pady=3).pack(side=LEFT, padx=10)
        Button(search_frame, text="🔄 Refresh", font=("Segoe UI", 10, "bold"),
               bg="#27AE60", fg="white", cursor="hand2", relief=FLAT,
               command=self.show, padx=15, pady=3).pack(side=LEFT, padx=5)

        # Table Frame
        table_frame = LabelFrame(right_panel, text=" Student List ",
                                 font=("Segoe UI", 11, "bold"),
                                 bg="white", fg="#1A3E6F", bd=2, relief=GROOVE)
        table_frame.pack(fill=BOTH, expand=True)

        self.C_frame = Frame(table_frame, bg="#F0F4F8")
        self.C_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        scrolly = Scrollbar(self.C_frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_frame, orient=HORIZONTAL)

        columns = ("roll", "name", "email", "gender", "dob", "contact",
                   "admission", "course", "state", "city", "pin", "address")
        self.course_table = ttk.Treeview(self.C_frame, columns=columns,
                                         xscrollcommand=scrollx.set,
                                         yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.course_table.xview)
        scrolly.config(command=self.course_table.yview)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                        background="#1A3E6F", foreground="white")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)

        self.course_table.heading("roll", text="Roll No")
        self.course_table.heading("name", text="Name")
        self.course_table.heading("email", text="Email")
        self.course_table.heading("gender", text="Gender")
        self.course_table.heading("dob", text="D.O.B")
        self.course_table.heading("contact", text="Contact")
        self.course_table.heading("admission", text="Admission")
        self.course_table.heading("course", text="Course")
        self.course_table.heading("state", text="State")
        self.course_table.heading("city", text="City")
        self.course_table.heading("pin", text="PIN")
        self.course_table.heading("address", text="Address")
        self.course_table["show"] = "headings"

        widths = [80, 150, 180, 80, 90, 100, 100, 120, 100, 100, 80, 200]
        for col, w in zip(columns, widths):
            self.course_table.column(col, width=w, anchor=W if col != "roll" else CENTER)

        self.course_table.pack(fill=BOTH, expand=1)
        self.course_table.bind("<ButtonRelease-1>", self.get_data)

    def _add_field(self, parent, label, variable, row):
        """Add a label + entry field with Enter navigation"""
        Label(parent, text=label, font=("Segoe UI", 11, "bold"),
              bg="white", fg="#333").grid(row=row, column=0, sticky="w", pady=(10, 2))
        entry = Entry(parent, textvariable=variable, font=("Segoe UI", 10),
                      bg="#F0F4F8", relief=SOLID, bd=1, width=25)
        entry.grid(row=row+1, column=0, sticky="ew", pady=(0, 10))
        entry.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(entry)
        return entry

    def _add_combo(self, parent, label, variable, row, values, readonly=False):
        """Add a label + combobox with Enter navigation"""
        Label(parent, text=label, font=("Segoe UI", 11, "bold"),
              bg="white", fg="#333").grid(row=row, column=0, sticky="w", pady=(10, 2))
        combo = ttk.Combobox(parent, textvariable=variable, font=("Segoe UI", 10),
                             state="readonly" if readonly else "readonly", width=23)
        if values:
            combo['values'] = values
            if not variable.get() and values:
                combo.current(0)
        combo.grid(row=row+1, column=0, sticky="ew", pady=(0, 10))
        combo.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(combo)
        return combo

    def _on_enter_pressed(self, event):
        current = event.widget
        try:
            idx = self.entry_fields.index(current)
            if idx < len(self.entry_fields) - 1:
                self.entry_fields[idx + 1].focus()
            else:
                self.txt_address.focus()
        except ValueError:
            pass
        return "break"

    def _on_enter_text(self, event):
        self.txt_address.insert(INSERT, "\n")
        return "break"

    def fetch_course(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM course")
            rows = cur.fetchall()
            self.course_list = [row[0] for row in rows]
            if hasattr(self, 'txt_course') and self.txt_course:
                self.txt_course['values'] = self.course_list
                if self.course_list:
                    self.txt_course.set(self.course_list[0])
                else:
                    self.txt_course.set("No courses")
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching courses: {str(ex)}")
        finally:
            con.close()

    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showwarning("Warning", "Please enter Roll No", parent=self.root)
                return
            cur.execute("SELECT * FROM student WHERE roll=?", (self.var_search.get(),))
            row = cur.fetchone()
            if row:
                self.course_table.delete(*self.course_table.get_children())
                self.course_table.insert('', END, values=row)
            else:
                messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def clear(self):
        self.var_rollno.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_admission.set("")
        self.var_course.set("")
        self.var_state.set("")
        self.var_city.set("")
        self.var_pin.set("")
        self.txt_address.delete('1.0', END)
        self.var_search.set("")
        self.show()

    def delete(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_rollno.get() == "":
                messagebox.showerror("Error", "Roll Number is required", parent=self.root)
                return
            cur.execute("SELECT * FROM result WHERE roll=?", (self.var_rollno.get(),))
            if cur.fetchone():
                op = messagebox.askyesno("Confirm",
                                         f"Student '{self.var_name.get()}' has results.\n"
                                         f"Deleting will also delete all results.\n\n"
                                         f"Do you want to proceed?",
                                         parent=self.root)
                if op:
                    cur.execute("DELETE FROM result WHERE roll=?", (self.var_rollno.get(),))
                    cur.execute("DELETE FROM student WHERE roll=?", (self.var_rollno.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Student and results deleted", parent=self.root)
                    self.clear()
                return
            op = messagebox.askyesno("Confirm", f"Delete student '{self.var_name.get()}'?", parent=self.root)
            if op:
                cur.execute("DELETE FROM student WHERE roll=?", (self.var_rollno.get(),))
                con.commit()
                messagebox.showinfo("Success", "Student deleted successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def get_data(self, ev):
        r = self.course_table.focus()
        content = self.course_table.item(r)
        row = content["values"]
        if row:
            self.var_rollno.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_gender.set(row[3])
            self.var_dob.set(row[4])
            self.var_contact.set(row[5])
            self.var_admission.set(row[6])
            self.var_course.set(row[7])
            self.var_state.set(row[8])
            self.var_city.set(row[9])
            self.var_pin.set(row[10])
            self.txt_address.delete('1.0', END)
            self.txt_address.insert(END, row[11])

    def add(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_rollno.get() == "" or self.var_name.get() == "":
                messagebox.showerror("Error", "Roll No and Name are required", parent=self.root)
                return
            cur.execute("SELECT * FROM student WHERE roll=?", (self.var_rollno.get(),))
            if cur.fetchone():
                messagebox.showerror("Error", "Roll Number already exists", parent=self.root)
                return
            cur.execute("""INSERT INTO student(roll, name, email, gender, dob, contact,
                          admission, course, state, city, pin, address)
                          VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (self.var_rollno.get(),
                         self.var_name.get(),
                         self.var_email.get(),
                         self.var_gender.get(),
                         self.var_dob.get(),
                         self.var_contact.get(),
                         self.var_admission.get(),
                         self.var_course.get(),
                         self.var_state.get(),
                         self.var_city.get(),
                         self.var_pin.get(),
                         self.txt_address.get('1.0', END).strip()))
            con.commit()
            messagebox.showinfo("Success", "Student added successfully", parent=self.root)
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def update(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_rollno.get() == "":
                messagebox.showerror("Error", "Roll Number is required", parent=self.root)
                return
            cur.execute("SELECT * FROM student WHERE roll=?", (self.var_rollno.get(),))
            if not cur.fetchone():
                messagebox.showerror("Error", "Student not found", parent=self.root)
                return
            cur.execute("""UPDATE student SET name=?, email=?, gender=?, dob=?, contact=?,
                          admission=?, course=?, state=?, city=?, pin=?, address=?
                          WHERE roll=?""",
                        (self.var_name.get(),
                         self.var_email.get(),
                         self.var_gender.get(),
                         self.var_dob.get(),
                         self.var_contact.get(),
                         self.var_admission.get(),
                         self.var_course.get(),
                         self.var_state.get(),
                         self.var_city.get(),
                         self.var_pin.get(),
                         self.txt_address.get('1.0', END).strip(),
                         self.var_rollno.get()))
            con.commit()
            messagebox.showinfo("Success", "Student updated successfully", parent=self.root)
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM student ORDER BY roll")
            rows = cur.fetchall()
            self.course_table.delete(*self.course_table.get_children())
            for row in rows:
                self.course_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
        finally:
            con.close()


if __name__ == "__main__":
    root= Tk()
    root.tk.call('tk', 'scaling', 1.4)
    obj = studentClass(root)
    root.mainloop()