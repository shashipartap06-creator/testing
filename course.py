from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
from create_db import create_db

class CourseClass:
    def __init__(self, root):
        self.root = root
        self.root.title("SRMS — Manage Courses")
        self.root.geometry("1300x650+80+80")
        self.root.config(bg="#F0F4F8")
        self.root.focus_force()

        # Title Bar
        self._create_title_bar()
        
        # Main Container
        main_frame = Frame(self.root, bg="#F0F4F8")
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=15)
        
        # Left Panel - Form
        left_panel = LabelFrame(main_frame, text=" Course Information ", 
                                font=("Segoe UI", 12, "bold"),
                                bg="white", fg="#1A3E6F", bd=2, relief=GROOVE)
        left_panel.pack(side=LEFT, fill=Y, padx=(0, 15), ipadx=10, ipady=10)
        
        # Variables
        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()
        self.var_search = StringVar()
        
        # Form Fields
        self._create_form_fields(left_panel)
        
        # Right Panel - Course List
        right_panel = Frame(main_frame, bg="#F0F4F8")
        right_panel.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Search Panel
        self._create_search_panel(right_panel)
        
        # Table Frame
        self._create_table(right_panel)
        
        # Load data
        self.show()
    
    def _create_title_bar(self):
        """Create modern title bar"""
        title_bar = Frame(self.root, bg="#1A3E6F", height=50)
        title_bar.pack(fill=X, side=TOP)
        title_bar.pack_propagate(False)
        
        Label(title_bar, text="📚  Manage Course Details",
              font=("Segoe UI", 18, "bold"), bg="#1A3E6F", fg="white").pack(side=LEFT, padx=20, pady=8)
    
    def _create_form_fields(self, parent):
        """Create input form fields"""
        # Course Name
        Label(parent, text="Course Name", font=("Segoe UI", 11, "bold"),
              bg="white", fg="#333").grid(row=0, column=0, padx=15, pady=(15, 5), sticky=W)
        self.txt_courseName = Entry(parent, textvariable=self.var_course,
                                    font=("Segoe UI", 11), bg="#F0F4F8", 
                                    relief=SOLID, bd=1, width=30)
        self.txt_courseName.grid(row=1, column=0, padx=15, pady=(0, 10), sticky=EW)
        
        # Duration
        Label(parent, text="Duration", font=("Segoe UI", 11, "bold"),
              bg="white", fg="#333").grid(row=2, column=0, padx=15, pady=(10, 5), sticky=W)
        Entry(parent, textvariable=self.var_duration,
              font=("Segoe UI", 11), bg="#F0F4F8", relief=SOLID, bd=1, width=30
              ).grid(row=3, column=0, padx=15, pady=(0, 10), sticky=EW)
        
        # Charges
        Label(parent, text="Charges (₹)", font=("Segoe UI", 11, "bold"),
              bg="white", fg="#333").grid(row=4, column=0, padx=15, pady=(10, 5), sticky=W)
        Entry(parent, textvariable=self.var_charges,
              font=("Segoe UI", 11), bg="#F0F4F8", relief=SOLID, bd=1, width=30
              ).grid(row=5, column=0, padx=15, pady=(0, 10), sticky=EW)
        
        # Description
        Label(parent, text="Description", font=("Segoe UI", 11, "bold"),
              bg="white", fg="#333").grid(row=6, column=0, padx=15, pady=(10, 5), sticky=W)
        self.txt_description = Text(parent, font=("Segoe UI", 10), 
                                    bg="#F0F4F8", relief=SOLID, bd=1, width=30, height=6)
        self.txt_description.grid(row=7, column=0, padx=15, pady=(0, 15), sticky=EW)
        
        # Buttons
        btn_frame = Frame(parent, bg="white")
        btn_frame.grid(row=8, column=0, padx=15, pady=(0, 15), sticky=EW)
        
        Button(btn_frame, text="💾 Save", font=("Segoe UI", 10, "bold"),
               bg="#27AE60", fg="white", cursor="hand2", relief=FLAT,
               command=self.add, padx=15, pady=5
               ).pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
        
        Button(btn_frame, text="✏️ Update", font=("Segoe UI", 10, "bold"),
               bg="#2B6CB0", fg="white", cursor="hand2", relief=FLAT,
               command=self.update, padx=15, pady=5
               ).pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
        
        Button(btn_frame, text="🗑 Delete", font=("Segoe UI", 10, "bold"),
               bg="#C0392B", fg="white", cursor="hand2", relief=FLAT,
               command=self.delete, padx=15, pady=5
               ).pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
        
        Button(btn_frame, text="✖ Clear", font=("Segoe UI", 10, "bold"),
               bg="#7F8C8D", fg="white", cursor="hand2", relief=FLAT,
               command=self.clear, padx=15, pady=5
               ).pack(side=LEFT, fill=X, expand=True)
        
        parent.columnconfigure(0, weight=1)
    
    def _create_search_panel(self, parent):
        """Create search panel"""
        search_frame = LabelFrame(parent, text=" Search Course ", 
                                  font=("Segoe UI", 11, "bold"),
                                  bg="white", fg="#1A3E6F", bd=2, relief=GROOVE)
        search_frame.pack(fill=X, pady=(0, 15), ipady=8)
        
        Label(search_frame, text="Course Name:", font=("Segoe UI", 10, "bold"),
              bg="white", fg="#333").pack(side=LEFT, padx=(15, 10))
        
        Entry(search_frame, textvariable=self.var_search,
              font=("Segoe UI", 10), bg="#F0F4F8", relief=SOLID, bd=1, width=25
              ).pack(side=LEFT, padx=5)
        
        Button(search_frame, text="🔍 Search", font=("Segoe UI", 10, "bold"),
               bg="#2B6CB0", fg="white", cursor="hand2", relief=FLAT,
               command=self.search, padx=15, pady=3
               ).pack(side=LEFT, padx=10)
        
        Button(search_frame, text="🔄 Refresh", font=("Segoe UI", 10, "bold"),
               bg="#27AE60", fg="white", cursor="hand2", relief=FLAT,
               command=self.show, padx=15, pady=3
               ).pack(side=LEFT, padx=5)
    
    def _create_table(self, parent):
        """Create treeview table"""
        table_frame = LabelFrame(parent, text=" Course List ", 
                                 font=("Segoe UI", 11, "bold"),
                                 bg="grey", fg="#1A3E6F", bd=2, relief=GROOVE)
        table_frame.pack(fill=BOTH, expand=True)
        
        # Scrollbars
        scrolly = Scrollbar(table_frame, orient=VERTICAL)
        scrollx = Scrollbar(table_frame, orient=HORIZONTAL)
        
        self.course_table = ttk.Treeview(table_frame,
                                         columns=("cid", "name", "duration", "charges", "description"),
                                         xscrollcommand=scrollx.set,
                                         yscrollcommand=scrolly.set)
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.course_table.xview)
        scrolly.config(command=self.course_table.yview)
        
        # Configure style
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                        background="#1A3E6F", foreground="grey")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)
        
        # Columns
        self.course_table.heading("cid", text="Course ID")
        self.course_table.heading("name", text="Course Name")
        self.course_table.heading("duration", text="Duration")
        self.course_table.heading("charges", text="Charges (₹)")
        self.course_table.heading("description", text="Description")
        
        self.course_table["show"] = "headings"
        
        self.course_table.column("cid", width=80, anchor=CENTER)
        self.course_table.column("name", width=180, anchor=W)
        self.course_table.column("duration", width=100, anchor=CENTER)
        self.course_table.column("charges", width=100, anchor=CENTER)
        self.course_table.column("description", width=350, anchor=W)
        
        self.course_table.pack(fill=BOTH, expand=1)
        
        # Bind selection
        self.course_table.bind("<ButtonRelease-1>", self.get_data)
    
    def search(self):
        """Search courses by name"""
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            search_term = self.var_search.get().strip()
            if search_term:
                cur.execute("SELECT * FROM course WHERE name LIKE ?", (f'%{search_term}%',))
            else:
                cur.execute("SELECT * FROM course")
            rows = cur.fetchall()
            self.course_table.delete(*self.course_table.get_children())
            for row in rows:
                self.course_table.insert('', END, values=row)
            if not rows and search_term:
                messagebox.showinfo("Info", "No courses found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()
    
    def clear(self):
        """Clear all fields"""
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete('1.0', END)
        self.txt_courseName.config(state=NORMAL)
        self.show()
    
    def delete(self):
        """Delete selected course"""
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showwarning("Warning", "Please select a course to delete", parent=self.root)
                return
            # Check if course is assigned to any student
            cur.execute("SELECT * FROM student WHERE course=?", (self.var_course.get(),))
            if cur.fetchone():
                messagebox.showwarning("Warning", f"Cannot delete '{self.var_course.get()}'\nThis course is assigned to students.", parent=self.root)
                return
            op = messagebox.askyesno("Confirm", f"Do you really want to delete course:\n'{self.var_course.get()}'?", parent=self.root)
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
        """Get selected row data"""
        self.txt_courseName.config(state='normal')
        r = self.course_table.focus()
        content = self.course_table.item(r)
        row = content["values"]
        if row:
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
            if self.var_course.get().strip() == "":
                messagebox.showwarning("Warning", "Course Name is required", parent=self.root)
                return
            if self.var_duration.get().strip() == "":
                messagebox.showwarning("Warning", "Duration is required", parent=self.root)
                return
            if self.var_charges.get().strip() == "":
                messagebox.showwarning("Warning", "Charges are required", parent=self.root)
                return
            
            # Check duplicate
            cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
            if cur.fetchone():
                messagebox.showerror("Error", "Course Name already exists", parent=self.root)
                return
            
            cur.execute("INSERT INTO course(name, duration, charges, description) VALUES(?,?,?,?)",
                       (self.var_course.get().strip(),
                        self.var_duration.get().strip(),
                        self.var_charges.get().strip(),
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
            if not cur.fetchone():
                messagebox.showerror("Error", "Course not found", parent=self.root)
                return
            cur.execute("UPDATE course SET duration=?, charges=?, description=? WHERE name=?",
                       (self.var_duration.get().strip(),
                        self.var_charges.get().strip(),
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
        """Display all courses"""
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM course ORDER BY name")
            rows = cur.fetchall()
            self.course_table.delete(*self.course_table.get_children())
            for row in rows:
                self.course_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    root= Tk()
    root.tk.call('tk', 'scaling', 1.4)
    obj = CourseClass(root)
    root.mainloop()