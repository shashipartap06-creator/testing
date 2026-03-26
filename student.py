from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# ── Colour palette (matching hi.py) ────────────────────────────────────────────
BG        = "#0F1C2E"
SIDEBAR   = "#0A1628"
CARD_BG   = "#162032"
TOPBAR    = "#111E30"
ACCENT    = "#2B6CB0"
ACCENT2   = "#1A3E6F"
GREEN     = "#1ABC9C"
ORANGE    = "#E8692A"
PURPLE    = "#7C3AED"
TEXT      = "#E8EDF4"
SUBTEXT   = "#8CA0B8"
WHITE     = "#FFFFFF"
SEP       = "#1E2E42"

FONT_TITLE  = ("Segoe UI", 11, "bold")
FONT_BODY   = ("Segoe UI", 10)

class studentClass:
    def __init__(self, root):
        self.root = root
        self.root.title("SRMS — Manage Students")
        self.root.geometry("1500x850+30+30")
        self.root.config(bg=BG)
        self.root.focus_force()

        # ── Variables ──────────────────────────────────────────────────────────
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_contact = StringVar()
        self.var_admission = StringVar()
        self.var_course = StringVar()
        self.var_state = StringVar()
        self.var_city = StringVar()
        self.var_pin = StringVar()
        self.var_search = StringVar()
        
        # Store all entry widgets for tab navigation
        self.entry_fields = []

        # ── Build UI ───────────────────────────────────────────────────────────
        self._build_layout()
        self.show()

    def _build_layout(self):
        # Title Bar
        title_bar = Frame(self.root, bg=ACCENT2, height=55)
        title_bar.pack(fill=X, side=TOP)
        Label(title_bar, text="  👨‍🎓  Manage Student Details",
              font=("Segoe UI", 18, "bold"), bg=ACCENT2, fg=WHITE).pack(side=LEFT, pady=10, padx=15)

        # Main body with horizontal split
        body = Frame(self.root, bg=BG)
        body.pack(fill=BOTH, expand=True, padx=20, pady=15)

        # ── Left Panel - Student Entry Form (40% width) ─────────────────────────
        left_panel = Frame(body, bg=CARD_BG, width=500)
        left_panel.pack(side=LEFT, fill=Y, padx=(0, 15))
        left_panel.pack_propagate(False)
        
        # Title inside left panel
        Label(left_panel, text="📝 STUDENT INFORMATION", font=("Segoe UI", 12, "bold"),
              bg=ACCENT2, fg=WHITE, pady=10).pack(fill=X)
        
        # Form container with scrollbar
        form_canvas = Canvas(left_panel, bg=CARD_BG, highlightthickness=0)
        form_scrollbar = Scrollbar(left_panel, orient=VERTICAL, command=form_canvas.yview)
        form_frame = Frame(form_canvas, bg=CARD_BG)
        
        form_canvas.configure(yscrollcommand=form_scrollbar.set)
        form_canvas.create_window((0, 0), window=form_frame, anchor="nw", width=480)
        form_frame.bind("<Configure>", lambda e: form_canvas.configure(scrollregion=form_canvas.bbox("all")))
        
        form_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        form_scrollbar.pack(side=RIGHT, fill=Y)
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            form_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        form_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Form fields with proper spacing
        fields = [
            ("Roll No.", self.var_roll),
            ("Full Name", self.var_name),
            ("Email", self.var_email),
            ("Gender", self.var_gender),
            ("Date of Birth (DD/MM/YYYY)", self.var_dob),
            ("Contact No.", self.var_contact),
            ("Admission Date", self.var_admission),
            ("Course", self.var_course),
            ("State", self.var_state),
            ("City", self.var_city),
            ("PIN Code", self.var_pin),
        ]
        
        # Create all fields with proper spacing and Enter key binding
        for i, (label, var) in enumerate(fields):
            Label(form_frame, text=label, font=FONT_TITLE,
                  bg=CARD_BG, fg=SUBTEXT).grid(row=i*2, column=0, padx=20, pady=(15, 5), sticky=W)
            entry = Entry(form_frame, textvariable=var, font=FONT_BODY,
                         bg="#2A3A4A", fg=TEXT, relief=SOLID, bd=1, width=35,
                         insertbackground=WHITE)
            entry.grid(row=i*2+1, column=0, padx=20, pady=(0, 10), sticky=EW)
            entry.bind("<Return>", self._on_enter_pressed)
            self.entry_fields.append(entry)
            form_frame.grid_columnconfigure(0, weight=1)
        
        # Address field
        addr_row = len(fields) * 2
        Label(form_frame, text="Address", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).grid(row=addr_row, column=0, padx=20, pady=(15, 5), sticky=W)
        
        self.txt_address = Text(form_frame, font=FONT_BODY, bg="#2A3A4A", 
                                fg=TEXT, relief=SOLID, bd=1, width=35, height=4,
                                insertbackground=WHITE)
        self.txt_address.grid(row=addr_row+1, column=0, padx=20, pady=(0, 15), sticky=EW)
        self.txt_address.bind("<Return>", self._on_enter_pressed_text)
        
        # Buttons
        btn_row = addr_row + 2
        btn_frame = Frame(form_frame, bg=CARD_BG)
        btn_frame.grid(row=btn_row, column=0, padx=20, pady=(10, 25), sticky=EW)
        
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)
        btn_frame.grid_columnconfigure(3, weight=1)
        
        btn_save = Button(btn_frame, text="💾 Save", font=FONT_TITLE,
                         bg=GREEN, fg=WHITE, cursor="hand2", relief=FLAT,
                         command=self.add, pady=8)
        btn_save.grid(row=0, column=0, padx=5, sticky=EW)
        
        btn_update = Button(btn_frame, text="✏️ Update", font=FONT_TITLE,
                           bg=ACCENT, fg=WHITE, cursor="hand2", relief=FLAT,
                           command=self.update, pady=8)
        btn_update.grid(row=0, column=1, padx=5, sticky=EW)
        
        btn_delete = Button(btn_frame, text="🗑 Delete", font=FONT_TITLE,
                           bg="#C0392B", fg=WHITE, cursor="hand2", relief=FLAT,
                           command=self.delete, pady=8)
        btn_delete.grid(row=0, column=2, padx=5, sticky=EW)
        
        btn_clear = Button(btn_frame, text="✖ Clear", font=FONT_TITLE,
                          bg="#7F8C8D", fg=WHITE, cursor="hand2", relief=FLAT,
                          command=self.clear, pady=8)
        btn_clear.grid(row=0, column=3, padx=5, sticky=EW)

        # ── Right Panel - Student List (60% width) ──────────────────────────────
        right_panel = Frame(body, bg=BG)
        right_panel.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Search Panel
        search_frame = Frame(right_panel, bg=CARD_BG, height=60)
        search_frame.pack(fill=X, pady=(0, 15))
        search_frame.pack_propagate(False)
        
        Label(search_frame, text="🔍 Search by Roll No:", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).pack(side=LEFT, padx=(15, 10), pady=15)
        
        self.search_entry = Entry(search_frame, textvariable=self.var_search,
                                   font=FONT_BODY, bg="#2A3A4A", fg=TEXT, relief=SOLID, bd=1, width=20,
                                   insertbackground=WHITE)
        self.search_entry.pack(side=LEFT, padx=5, pady=15)
        self.search_entry.bind("<Return>", lambda e: self.search())
        
        btn_search = Button(search_frame, text="Search", font=FONT_TITLE,
                           bg=ACCENT, fg=WHITE, cursor="hand2", relief=FLAT,
                           command=self.search, padx=20)
        btn_search.pack(side=LEFT, padx=10, pady=15)
        
        btn_refresh = Button(search_frame, text="Refresh", font=FONT_TITLE,
                            bg=GREEN, fg=WHITE, cursor="hand2", relief=FLAT,
                            command=self.show, padx=20)
        btn_refresh.pack(side=LEFT, padx=5, pady=15)
        
        # Table Frame
        table_frame = Frame(right_panel, bg=CARD_BG)
        table_frame.pack(fill=BOTH, expand=True)
        
        # Treeview with scrollbars
        tree_container = Frame(table_frame, bg=BG)
        tree_container.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        scrolly = Scrollbar(tree_container, orient=VERTICAL)
        scrollx = Scrollbar(tree_container, orient=HORIZONTAL)
        
        # Define columns
        columns = ("roll", "name", "email", "gender", "dob", "contact", 
                   "admission", "course", "state", "city", "pin", "address")
        
        self.student_table = ttk.Treeview(tree_container, columns=columns,
                                          xscrollcommand=scrollx.set,
                                          yscrollcommand=scrolly.set,
                                          height=18, show="headings")
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.student_table.xview)
        scrolly.config(command=self.student_table.yview)
        
        # Configure Treeview style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                        background=ACCENT2, foreground=WHITE, relief=FLAT)
        style.configure("Treeview", font=FONT_BODY, rowheight=28,
                        background=CARD_BG, foreground=TEXT, fieldbackground=CARD_BG)
        style.map('Treeview', background=[('selected', ACCENT)])
        
        # Column configurations
        col_config = {
            "roll": ("Roll No", 80, CENTER),
            "name": ("Name", 150, W),
            "email": ("Email", 180, W),
            "gender": ("Gender", 80, CENTER),
            "dob": ("DOB", 90, CENTER),
            "contact": ("Contact", 110, CENTER),
            "admission": ("Admission", 100, CENTER),
            "course": ("Course", 120, W),
            "state": ("State", 100, W),
            "city": ("City", 100, W),
            "pin": ("PIN", 80, CENTER),
            "address": ("Address", 200, W)
        }
        
        for col, (text, width, anchor) in col_config.items():
            self.student_table.heading(col, text=text)
            self.student_table.column(col, width=width, anchor=anchor)
        
        self.student_table.pack(fill=BOTH, expand=True)
        
        # Bind selection event
        self.student_table.bind("<ButtonRelease-1>", self.get_data)
        
        # Configure row colors
        self.student_table.tag_configure("odd", background="#1E2E42")
        self.student_table.tag_configure("even", background="#162032")
        
        # Bind Enter key on buttons
        btn_save.bind("<Return>", lambda e: self.add())
        btn_update.bind("<Return>", lambda e: self.update())
        btn_delete.bind("<Return>", lambda e: self.delete())
        btn_clear.bind("<Return>", lambda e: self.clear())
        btn_search.bind("<Return>", lambda e: self.search())
        btn_refresh.bind("<Return>", lambda e: self.show())

    def _on_enter_pressed(self, event):
        """Handle Enter key press - move to next field"""
        current = event.widget
        try:
            index = self.entry_fields.index(current)
            if index < len(self.entry_fields) - 1:
                self.entry_fields[index + 1].focus()
            else:
                # If last field, focus on text area
                self.txt_address.focus()
        except ValueError:
            pass
        return "break"

    def _on_enter_pressed_text(self, event):
        """Handle Enter key in text area - move to Save button"""
        # Check if Ctrl+Enter was pressed
        if event.state & 0x4:  # Ctrl key
            self.add()  # Save on Ctrl+Enter
        else:
            # Just insert newline normally
            self.txt_address.insert(INSERT, "\n")
        return "break"

    def search(self):
        """Search student by roll number"""
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showwarning("Warning", "Please enter Roll No", parent=self.root)
            else:
                cur.execute("SELECT * FROM student WHERE roll=?", (self.var_search.get(),))
                row = cur.fetchone()
                if row:
                    self.clear()
                    self.var_roll.set(row[0])
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
                    self.txt_address.insert('1.0', row[11] if len(row) > 11 else "")
                    # Focus on first field after search
                    if self.entry_fields:
                        self.entry_fields[0].focus()
                else:
                    messagebox.showerror("Error", "Student not found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        """Clear all input fields"""
        self.var_roll.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("")
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_admission.set("")
        self.var_course.set("")
        self.var_state.set("")
        self.var_city.set("")
        self.var_pin.set("")
        self.var_search.set("")
        self.txt_address.delete('1.0', END)
        # Focus on first field after clear
        if self.entry_fields:
            self.entry_fields[0].focus()

    def delete(self):
        """Delete selected student"""
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_roll.get() == "":
                messagebox.showwarning("Warning", "Please select a student to delete", parent=self.root)
            else:
                cur.execute("SELECT * FROM result WHERE roll=?", (self.var_roll.get(),))
                results = cur.fetchone()
                
                if results:
                    op = messagebox.askyesno("Confirm",
                                           f"Student '{self.var_name.get()}' has results.\n"
                                           f"Deleting will also delete all results.\n\n"
                                           f"Do you want to proceed?",
                                           parent=self.root)
                    if op:
                        cur.execute("DELETE FROM result WHERE roll=?", (self.var_roll.get(),))
                        cur.execute("DELETE FROM student WHERE roll=?", (self.var_roll.get(),))
                        con.commit()
                        messagebox.showinfo("Success", "Student and their results deleted", parent=self.root)
                        self.clear()
                        self.show()
                else:
                    op = messagebox.askyesno("Confirm",
                                           f"Do you really want to delete student:\n'{self.var_name.get()}'?",
                                           parent=self.root)
                    if op:
                        cur.execute("DELETE FROM student WHERE roll=?", (self.var_roll.get(),))
                        con.commit()
                        messagebox.showinfo("Success", "Student deleted successfully", parent=self.root)
                        self.clear()
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        """Get selected student data and populate form"""
        r = self.student_table.focus()
        content = self.student_table.item(r)
        row = content["values"]
        
        if row:
            self.clear()
            self.var_roll.set(row[0])
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
            if len(row) > 11:
                self.txt_address.insert('1.0', row[11])
            # Focus on first field after loading
            if self.entry_fields:
                self.entry_fields[0].focus()

    def add(self):
        """Add new student"""
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_roll.get() == "" or self.var_name.get() == "":
                messagebox.showwarning("Warning", "Roll No and Name are required", parent=self.root)
                return
            
            cur.execute("SELECT * FROM student WHERE roll=?", (self.var_roll.get(),))
            if cur.fetchone():
                messagebox.showerror("Error", "Roll No already exists", parent=self.root)
            else:
                cur.execute("""INSERT INTO student(roll, name, email, gender, dob, contact, 
                              admission, course, state, city, pin, address) 
                              VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                           (self.var_roll.get(), self.var_name.get(), self.var_email.get(),
                            self.var_gender.get(), self.var_dob.get(), self.var_contact.get(),
                            self.var_admission.get(), self.var_course.get(), self.var_state.get(),
                            self.var_city.get(), self.var_pin.get(),
                            self.txt_address.get('1.0', END).strip()))
                con.commit()
                messagebox.showinfo("Success", "Student added successfully", parent=self.root)
                self.clear()
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def update(self):
        """Update existing student"""
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_roll.get() == "":
                messagebox.showwarning("Warning", "Please select a student to update", parent=self.root)
                return
            
            cur.execute("SELECT * FROM student WHERE roll=?", (self.var_roll.get(),))
            if not cur.fetchone():
                messagebox.showerror("Error", "Student not found", parent=self.root)
            else:
                cur.execute("""UPDATE student SET name=?, email=?, gender=?, dob=?, contact=?, 
                              admission=?, course=?, state=?, city=?, pin=?, address=? 
                              WHERE roll=?""",
                           (self.var_name.get(), self.var_email.get(), self.var_gender.get(),
                            self.var_dob.get(), self.var_contact.get(), self.var_admission.get(),
                            self.var_course.get(), self.var_state.get(), self.var_city.get(),
                            self.var_pin.get(), self.txt_address.get('1.0', END).strip(),
                            self.var_roll.get()))
                con.commit()
                messagebox.showinfo("Success", "Student updated successfully", parent=self.root)
                self.clear()
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        """Display all students in the table"""
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM student ORDER BY roll")
            rows = cur.fetchall()
            self.student_table.delete(*self.student_table.get_children())
            
            for i, row in enumerate(rows):
                tag = "even" if i % 2 == 0 else "odd"
                self.student_table.insert('', END, values=row, tags=(tag,))
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = studentClass(root)
    root.mainloop()