from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# ── Modern Color Palette (matching hi.py) ─────────────────────────────────────
BG        = "#0F1C2E"   # Deep navy background
SIDEBAR   = "#0A1628"   # Darker sidebar
CARD_BG   = "#162032"   # Card backgrounds
TOPBAR    = "#111E30"   # Top navigation bar
ACCENT    = "#4361EE"   # Modern blue accent
ACCENT2   = "#3A56D4"   # Darker blue for hover states
GREEN     = "#06D6A0"   # Vibrant green
ORANGE    = "#FF9E00"   # Modern amber
PURPLE    = "#8338EC"   # Vibrant purple
TEXT      = "#FFFFFF"   # Primary text
SUBTEXT   = "#A0AEC0"   # Secondary text
WHITE     = "#FFFFFF"
SEP       = "#2D3748"   # Separator lines
HOVER     = "#1E2E42"   # Hover effect color
LIGHT_BG  = "#1E2E42"   # Lighter background for entries

FONT_TITLE  = ("Segoe UI", 12, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)

class CourseClass:
    def __init__(self, root):
        self.root = root
        self.root.title("SRMS — Manage Courses")
        self.root.geometry("1500x750+30+30")
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
        title_bar = Frame(self.root, bg=ACCENT2, height=60)
        title_bar.pack(fill=X, side=TOP)
        
        # Gradient effect in title bar
        title_canvas = Canvas(title_bar, bg=ACCENT2, highlightthickness=0, height=60)
        title_canvas.pack(fill=BOTH, expand=True)
        
        for i in range(60):
            r = int(58 + (i * 0.2))
            g = int(86 - (i * 0.1))
            b = int(212 - (i * 0.8))
            color = f"#{r:02x}{g:02x}{b:02x}"
            title_canvas.create_line(0, i, title_bar.winfo_width(), i, fill=color, width=1)
        
        Label(title_bar, text="  📚  Manage Course Details",
              font=("Segoe UI", 18, "bold"), bg=ACCENT2, fg=WHITE).place(x=15, y=15)

        # Main body
        body = Frame(self.root, bg=BG)
        body.pack(fill=BOTH, expand=True, padx=20, pady=15)

        # ── Left Panel - Course Entry Form ──────────────────────────────────────
        left_panel = Frame(body, bg=CARD_BG, width=450)
        left_panel.pack(side=LEFT, fill=Y, padx=(0, 15))
        left_panel.pack_propagate(False)
        
        # Title inside left panel
        Label(left_panel, text="📝 COURSE INFORMATION", font=("Segoe UI", 13, "bold"),
              bg=ACCENT, fg=WHITE, pady=12).pack(fill=X)
        
        # Form container with scrollbar
        form_canvas = Canvas(left_panel, bg=CARD_BG, highlightthickness=0)
        form_scrollbar = Scrollbar(left_panel, orient=VERTICAL, command=form_canvas.yview)
        form_frame = Frame(form_canvas, bg=CARD_BG)
        
        form_canvas.configure(yscrollcommand=form_scrollbar.set)
        form_canvas.create_window((0, 0), window=form_frame, anchor="nw", width=430)
        form_frame.bind("<Configure>", lambda e: form_canvas.configure(scrollregion=form_canvas.bbox("all")))
        
        form_canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=10)
        form_scrollbar.pack(side=RIGHT, fill=Y)
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            form_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        form_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Course Name
        Label(form_frame, text="Course Name", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).grid(row=0, column=0, padx=20, pady=(15, 5), sticky=W)
        self.txt_courseName = Entry(form_frame, textvariable=self.var_course, font=FONT_BODY,
                                    bg=LIGHT_BG, fg=WHITE, relief=SOLID, bd=1, width=35,
                                    insertbackground=WHITE)
        self.txt_courseName.grid(row=1, column=0, padx=20, pady=(0, 15), sticky=EW)
        self.txt_courseName.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_courseName)
        
        # Duration
        Label(form_frame, text="Duration", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).grid(row=2, column=0, padx=20, pady=(5, 5), sticky=W)
        self.txt_duration = Entry(form_frame, textvariable=self.var_duration, font=FONT_BODY,
                                  bg=LIGHT_BG, fg=WHITE, relief=SOLID, bd=1, width=35,
                                  insertbackground=WHITE)
        self.txt_duration.grid(row=3, column=0, padx=20, pady=(0, 15), sticky=EW)
        self.txt_duration.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_duration)
        
        # Charges
        Label(form_frame, text="Charges (₹)", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).grid(row=4, column=0, padx=20, pady=(5, 5), sticky=W)
        self.txt_charges = Entry(form_frame, textvariable=self.var_charges, font=FONT_BODY,
                                 bg=LIGHT_BG, fg=WHITE, relief=SOLID, bd=1, width=35,
                                 insertbackground=WHITE)
        self.txt_charges.grid(row=5, column=0, padx=20, pady=(0, 15), sticky=EW)
        self.txt_charges.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_charges)
        
        # Description
        Label(form_frame, text="Description", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).grid(row=6, column=0, padx=20, pady=(5, 5), sticky=W)
        self.txt_description = Text(form_frame, font=FONT_BODY, bg=LIGHT_BG,
                                    fg=WHITE, relief=SOLID, bd=1, width=35, height=6,
                                    insertbackground=WHITE)
        self.txt_description.grid(row=7, column=0, padx=20, pady=(0, 20), sticky=EW)
        self.txt_description.bind("<Return>", self._on_enter_pressed_text)
        
        # Buttons
        btn_frame = Frame(form_frame, bg=CARD_BG)
        btn_frame.grid(row=8, column=0, padx=20, pady=(0, 20), sticky=EW)
        
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)
        btn_frame.grid_columnconfigure(3, weight=1)
        
        btn_save = Button(btn_frame, text="💾 Save", font=FONT_TITLE,
                         bg=GREEN, fg=WHITE, cursor="hand2", relief=FLAT,
                         activebackground="#05b88a", command=self.add, pady=10)
        btn_save.grid(row=0, column=0, padx=5, sticky=EW)
        btn_save.bind("<Return>", lambda e: self.add())
        
        btn_update = Button(btn_frame, text="✏️ Update", font=FONT_TITLE,
                           bg=ACCENT, fg=WHITE, cursor="hand2", relief=FLAT,
                           activebackground=ACCENT2, command=self.update, pady=10)
        btn_update.grid(row=0, column=1, padx=5, sticky=EW)
        btn_update.bind("<Return>", lambda e: self.update())
        
        btn_delete = Button(btn_frame, text="🗑 Delete", font=FONT_TITLE,
                           bg="#E53E3E", fg=WHITE, cursor="hand2", relief=FLAT,
                           activebackground="#C53030", command=self.delete, pady=10)
        btn_delete.grid(row=0, column=2, padx=5, sticky=EW)
        btn_delete.bind("<Return>", lambda e: self.delete())
        
        btn_clear = Button(btn_frame, text="✖ Clear", font=FONT_TITLE,
                          bg="#4A5568", fg=WHITE, cursor="hand2", relief=FLAT,
                          activebackground="#2D3748", command=self.clear, pady=10)
        btn_clear.grid(row=0, column=3, padx=5, sticky=EW)
        btn_clear.bind("<Return>", lambda e: self.clear())
        
        form_frame.grid_columnconfigure(0, weight=1)

        # ── Right Panel - Course List ──────────────────────────────────────────
        right_panel = Frame(body, bg=BG)
        right_panel.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Search Panel
        search_frame = Frame(right_panel, bg=CARD_BG, height=70)
        search_frame.pack(fill=X, pady=(0, 15))
        search_frame.pack_propagate(False)
        
        Label(search_frame, text="🔍 Search by Course Name:", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).pack(side=LEFT, padx=(20, 10), pady=20)
        
        self.search_entry = Entry(search_frame, textvariable=self.var_search,
                                   font=FONT_BODY, bg=LIGHT_BG, fg=WHITE, 
                                   relief=SOLID, bd=1, width=28,
                                   insertbackground=WHITE)
        self.search_entry.pack(side=LEFT, padx=5, pady=20)
        self.search_entry.bind("<Return>", lambda e: self.search())
        
        btn_search = Button(search_frame, text="Search", font=FONT_TITLE,
                           bg=ACCENT, fg=WHITE, cursor="hand2", relief=FLAT,
                           activebackground=ACCENT2, command=self.search, padx=25, pady=6)
        btn_search.pack(side=LEFT, padx=10, pady=20)
        btn_search.bind("<Return>", lambda e: self.search())
        
        btn_refresh = Button(search_frame, text="Refresh", font=FONT_TITLE,
                            bg=GREEN, fg=WHITE, cursor="hand2", relief=FLAT,
                            activebackground="#05b88a", command=self.show, padx=25, pady=6)
        btn_refresh.pack(side=LEFT, padx=5, pady=20)
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
                                         height=12, show="headings")
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.course_table.xview)
        scrolly.config(command=self.course_table.yview)
        
        # Configure Treeview style for dark theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"),
                        background=ACCENT, foreground=WHITE, relief=FLAT)
        style.configure("Treeview", font=FONT_BODY, rowheight=32,
                        background=CARD_BG, foreground=TEXT, fieldbackground=CARD_BG)
        style.map('Treeview', background=[('selected', ACCENT2)])
        
        # Column configurations
        col_config = {
            "cid": ("Course ID", 80, CENTER),
            "name": ("Course Name", 250, W),
            "duration": ("Duration", 120, CENTER),
            "charges": ("Charges (₹)", 120, CENTER),
            "description": ("Description", 450, W)
        }
        
        for col, (text, width, anchor) in col_config.items():
            self.course_table.heading(col, text=text)
            self.course_table.column(col, width=width, anchor=anchor)
        
        self.course_table.pack(fill=BOTH, expand=True)
        
        # Bind selection event
        self.course_table.bind("<ButtonRelease-1>", self.get_data)
        
        # Configure tag for row colors
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
                self.txt_description.focus()
        except ValueError:
            pass
        return "break"

    def _on_enter_pressed_text(self, event):
        """Handle Enter key in text area"""
        if event.state & 0x4:  # Ctrl key
            self.add()
        else:
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