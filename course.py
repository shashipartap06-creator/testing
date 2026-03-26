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

class CourseClass:
    def __init__(self, root):
        self.root = root
        self.root.title("SRMS — Manage Courses")
        self.root.geometry("1500x700+30+30")
        self.root.config(bg=BG)
        self.root.focus_force()

        # ── Variables ──────────────────────────────────────────────────────────
        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()
        self.var_search = StringVar()
        self.var_cid = StringVar()
        
        # Store all entry widgets for tab navigation
        self.entry_fields = []

        # ── Build UI ───────────────────────────────────────────────────────────
        self._build_layout()
        self.show()

    def _build_layout(self):
        # Title Bar
        title_bar = Frame(self.root, bg=ACCENT2, height=55)
        title_bar.pack(fill=X, side=TOP)
        Label(title_bar, text="  📚  Manage Course Details",
              font=("Segoe UI", 18, "bold"), bg=ACCENT2, fg=WHITE).pack(side=LEFT, pady=10, padx=15)

        # Main body
        body = Frame(self.root, bg=BG)
        body.pack(fill=BOTH, expand=True, padx=20, pady=15)

        # ── Left Panel - Course Entry Form ──────────────────────────────────────
        left_panel = Frame(body, bg=CARD_BG, width=450)
        left_panel.pack(side=LEFT, fill=Y, padx=(0, 15))
        left_panel.pack_propagate(False)
        
        # Title inside left panel
        Label(left_panel, text="📝 COURSE INFORMATION", font=("Segoe UI", 12, "bold"),
              bg=ACCENT2, fg=WHITE, pady=10).pack(fill=X)
        
        # Form container
        form_frame = Frame(left_panel, bg=CARD_BG)
        form_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Course Name
        Label(form_frame, text="Course Name", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).grid(row=0, column=0, padx=10, pady=(15, 5), sticky=W)
        self.txt_courseName = Entry(form_frame, textvariable=self.var_course, font=FONT_BODY,
                                    bg="#2A3A4A", fg=TEXT, relief=SOLID, bd=1, width=35,
                                    insertbackground=WHITE)
        self.txt_courseName.grid(row=1, column=0, padx=10, pady=(0, 15), sticky=EW)
        self.txt_courseName.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_courseName)
        
        # Duration
        Label(form_frame, text="Duration", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).grid(row=2, column=0, padx=10, pady=(5, 5), sticky=W)
        self.txt_duration = Entry(form_frame, textvariable=self.var_duration, font=FONT_BODY,
                                  bg="#2A3A4A", fg=TEXT, relief=SOLID, bd=1, width=35,
                                  insertbackground=WHITE)
        self.txt_duration.grid(row=3, column=0, padx=10, pady=(0, 15), sticky=EW)
        self.txt_duration.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_duration)
        
        # Charges
        Label(form_frame, text="Charges (₹)", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).grid(row=4, column=0, padx=10, pady=(5, 5), sticky=W)
        self.txt_charges = Entry(form_frame, textvariable=self.var_charges, font=FONT_BODY,
                                 bg="#2A3A4A", fg=TEXT, relief=SOLID, bd=1, width=35,
                                 insertbackground=WHITE)
        self.txt_charges.grid(row=5, column=0, padx=10, pady=(0, 15), sticky=EW)
        self.txt_charges.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_charges)
        
        # Description
        Label(form_frame, text="Description", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).grid(row=6, column=0, padx=10, pady=(5, 5), sticky=W)
        self.txt_description = Text(form_frame, font=FONT_BODY, bg="#2A3A4A",
                                    fg=TEXT, relief=SOLID, bd=1, width=35, height=5,
                                    insertbackground=WHITE)
        self.txt_description.grid(row=7, column=0, padx=10, pady=(0, 20), sticky=EW)
        self.txt_description.bind("<Return>", self._on_enter_pressed_text)
        
        # Buttons
        btn_frame = Frame(form_frame, bg=CARD_BG)
        btn_frame.grid(row=8, column=0, padx=10, pady=(0, 15), sticky=EW)
        
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
        
        # Bind Enter key on buttons
        btn_save.bind("<Return>", lambda e: self.add())
        btn_update.bind("<Return>", lambda e: self.update())
        btn_delete.bind("<Return>", lambda e: self.delete())
        btn_clear.bind("<Return>", lambda e: self.clear())
        
        form_frame.grid_columnconfigure(0, weight=1)

        # ── Right Panel - Course List ──────────────────────────────────────────
        right_panel = Frame(body, bg=BG)
        right_panel.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Search Panel
        search_frame = Frame(right_panel, bg=CARD_BG, height=60)
        search_frame.pack(fill=X, pady=(0, 15))
        search_frame.pack_propagate(False)
        
        Label(search_frame, text="🔍 Search by Course Name:", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).pack(side=LEFT, padx=(15, 10), pady=15)
        
        self.search_entry = Entry(search_frame, textvariable=self.var_search,
                                   font=FONT_BODY, bg="#2A3A4A", fg=TEXT, relief=SOLID, bd=1, width=25,
                                   insertbackground=WHITE)
        self.search_entry.pack(side=LEFT, padx=5, pady=15)
        self.search_entry.bind("<Return>", lambda e: self.search())
        
        btn_search = Button(search_frame, text="Search", font=FONT_TITLE,
                           bg=ACCENT, fg=WHITE, cursor="hand2", relief=FLAT,
                           command=self.search, padx=20)
        btn_search.pack(side=LEFT, padx=10, pady=15)
        btn_search.bind("<Return>", lambda e: self.search())
        
        btn_refresh = Button(search_frame, text="Refresh", font=FONT_TITLE,
                            bg=GREEN, fg=WHITE, cursor="hand2", relief=FLAT,
                            command=self.show, padx=20)
        btn_refresh.pack(side=LEFT, padx=5, pady=15)
        btn_refresh.bind("<Return>", lambda e: self.show())
        
        # Course Table
        table_frame = Frame(right_panel, bg=CARD_BG)
        table_frame.pack(fill=BOTH, expand=True)
        
        # Treeview with scrollbars
        tree_container = Frame(table_frame, bg=BG)
        tree_container.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        scrolly = Scrollbar(tree_container, orient=VERTICAL)
        scrollx = Scrollbar(tree_container, orient=HORIZONTAL)
        
        # Define columns
        columns = ("cid", "name", "duration", "charges", "description")
        
        self.course_table = ttk.Treeview(tree_container, columns=columns,
                                         xscrollcommand=scrollx.set,
                                         yscrollcommand=scrolly.set,
                                         height=15, show="headings")
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.course_table.xview)
        scrolly.config(command=self.course_table.yview)
        
        # Configure Treeview style for dark theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                        background=ACCENT2, foreground=WHITE, relief=FLAT)
        style.configure("Treeview", font=FONT_BODY, rowheight=28,
                        background=CARD_BG, foreground=TEXT, fieldbackground=CARD_BG)
        style.map('Treeview', background=[('selected', ACCENT)])
        
        # Column configurations
        col_config = {
            "cid": ("Course ID", 80, CENTER),
            "name": ("Course Name", 200, W),
            "duration": ("Duration", 120, CENTER),
            "charges": ("Charges (₹)", 120, CENTER),
            "description": ("Description", 500, W)
        }
        
        for col, (text, width, anchor) in col_config.items():
            self.course_table.heading(col, text=text)
            self.course_table.column(col, width=width, anchor=anchor)
        
        self.course_table.pack(fill=BOTH, expand=True)
        
        # Bind selection event
        self.course_table.bind("<ButtonRelease-1>", self.get_data)
        
        # Configure row colors
        self.course_table.tag_configure("odd", background="#1E2E42")
        self.course_table.tag_configure("even", background="#162032")

    def _on_enter_pressed(self, event):
        """Handle Enter key press - move to next field"""
        current = event.widget
        try:
            index = self.entry_fields.index(current)
            if index < len(self.entry_fields) - 1:
                self.entry_fields[index + 1].focus()
            else:
                # If last field, focus on text area
                self.txt_description.focus()
        except ValueError:
            pass
        return "break"

    def _on_enter_pressed_text(self, event):
        """Handle Enter key in text area - move to Save button or add newline"""
        # Check if Ctrl+Enter was pressed
        if event.state & 0x4:  # Ctrl key
            self.add()  # Save on Ctrl+Enter
        else:
            # Just insert newline normally
            self.txt_description.insert(INSERT, "\n")
        return "break"

    def search(self):
        """Search courses by name"""
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            search_term = self.var_search.get()
            if search_term:
                cur.execute("SELECT * FROM course WHERE name LIKE ?", (f'%{search_term}%',))
            else:
                cur.execute("SELECT * FROM course")
            
            rows = cur.fetchall()
            self.course_table.delete(*self.course_table.get_children())
            
            for i, row in enumerate(rows):
                tag = "even" if i % 2 == 0 else "odd"
                self.course_table.insert('', END, values=row, tags=(tag,))
            
            if not rows and search_term:
                messagebox.showinfo("Info", "No courses found", parent=self.root)
            
            # Focus on first field after search
            if self.entry_fields:
                self.entry_fields[0].focus()
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        """Clear all input fields"""
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.var_cid.set("")
        self.txt_description.delete('1.0', END)
        self.txt_courseName.config(state=NORMAL)
        # Focus on first field after clear
        if self.entry_fields:
            self.entry_fields[0].focus()
        self.show()

    def delete(self):
        """Delete selected course"""
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showwarning("Warning", "Please select a course to delete", parent=self.root)
            else:
                # Check if course is being used in student table
                cur.execute("SELECT * FROM student WHERE course=?", (self.var_course.get(),))
                students = cur.fetchone()
                
                if students:
                    messagebox.showwarning("Warning",
                                         f"Cannot delete '{self.var_course.get()}'\n"
                                         f"This course is assigned to students.\n"
                                         f"Please reassign students first.",
                                         parent=self.root)
                    return
                
                op = messagebox.askyesno("Confirm",
                                        f"Do you really want to delete course:\n'{self.var_course.get()}'?",
                                        parent=self.root)
                if op:
                    cur.execute("DELETE FROM course WHERE name=?", (self.var_course.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Course deleted successfully", parent=self.root)
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        """Get selected course data and populate form"""
        self.txt_courseName.config(state='normal')
        r = self.course_table.focus()
        content = self.course_table.item(r)
        row = content["values"]
        
        if row:
            self.clear()
            self.var_cid.set(row[0])
            self.var_course.set(row[1])
            self.var_duration.set(row[2])
            self.var_charges.set(row[3])
            self.txt_description.delete('1.0', END)
            self.txt_description.insert('1.0', row[4])
            self.txt_courseName.config(state='readonly')
            # Focus on first field after loading
            if self.entry_fields:
                self.entry_fields[0].focus()

    def add(self):
        """Add new course"""
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showwarning("Warning", "Course Name is required", parent=self.root)
                return
            
            if self.var_duration.get() == "":
                messagebox.showwarning("Warning", "Duration is required", parent=self.root)
                return
            
            if self.var_charges.get() == "":
                messagebox.showwarning("Warning", "Charges are required", parent=self.root)
                return
            
            # Check if course already exists
            cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
            row = cur.fetchone()
            
            if row:
                messagebox.showerror("Error", "Course Name already exists", parent=self.root)
            else:
                cur.execute("INSERT INTO course(name, duration, charges, description) VALUES(?,?,?,?)",
                           (self.var_course.get(),
                            self.var_duration.get(),
                            self.var_charges.get(),
                            self.txt_description.get('1.0', END).strip()))
                con.commit()
                messagebox.showinfo("Success", "Course added successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def update(self):
        """Update existing course"""
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showwarning("Warning", "Please select a course to update", parent=self.root)
                return
            
            # Check if course exists
            cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
            row = cur.fetchone()
            
            if not row:
                messagebox.showerror("Error", "Course not found", parent=self.root)
            else:
                cur.execute("UPDATE course SET duration=?, charges=?, description=? WHERE name=?",
                           (self.var_duration.get(),
                            self.var_charges.get(),
                            self.txt_description.get('1.0', END).strip(),
                            self.var_course.get()))
                con.commit()
                messagebox.showinfo("Success", "Course updated successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        """Display all courses in the table"""
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM course ORDER BY name")
            rows = cur.fetchall()
            self.course_table.delete(*self.course_table.get_children())
            
            for i, row in enumerate(rows):
                tag = "even" if i % 2 == 0 else "odd"
                self.course_table.insert('', END, values=row, tags=(tag,))
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = CourseClass(root)
    root.mainloop()