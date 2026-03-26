from tkinter import *
from PIL import Image, ImageTk  # pip install pillow
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from create_db import create_db
from result import resultClass
from datetime import datetime

class reportClass:
    def __init__(self, root):
        self.root = root
        self.root.title("STUDENT RESULT MANAGEMENT SYSTEM")
        self.root.geometry("1200x700+60+30")
        self.root.config(bg="#F0F4F8")
        self.root.focus_force()

        # ── Title Bar ──────────────────────────────────────────────────────
        title_bar = Frame(self.root, bg="#1A3E6F", height=55)
        title_bar.pack(fill=X, side=TOP)
        Label(title_bar, text="  📊  View Student Results",
              font=("Segoe UI", 18, "bold"), bg="#1A3E6F", fg="white").pack(side=LEFT, pady=10, padx=15)

        # ── Main body ──────────────────────────────────────────────────────
        body = Frame(self.root, bg="#F0F4F8")
        body.pack(fill=BOTH, expand=True, padx=20, pady=15)

        # ── Search Panel ───────────────────────────────────────────────────
        search_frame = LabelFrame(body, text=" Search Student ", font=("Segoe UI", 12, "bold"),
                                  bg="#F0F4F8", fg="#1A3E6F", bd=2, relief=GROOVE)
        search_frame.pack(fill=X, pady=(0, 15), ipady=10)

        self.var_search = StringVar()
        
        Label(search_frame, text="Roll Number:", font=("Segoe UI", 12, "bold"),
              bg="#F0F4F8", fg="#444").pack(side=LEFT, padx=(20, 10))
        
        txt_search = Entry(search_frame, textvariable=self.var_search,
                          font=("Segoe UI", 12), bg="white", relief=SOLID, bd=1, width=20)
        txt_search.pack(side=LEFT, padx=5)
        
        btn_search = Button(search_frame, text="🔍 Search", font=("Segoe UI", 11, "bold"),
                           bg="#2B6CB0", fg="white", cursor="hand2",
                           activebackground="#1A3E6F", relief=FLAT,
                           command=self.search, padx=15, pady=5)
        btn_search.pack(side=LEFT, padx=10)
        
        btn_clear = Button(search_frame, text="✖ Clear", font=("Segoe UI", 11, "bold"),
                          bg="#7F8C8D", fg="white", cursor="hand2",
                          activebackground="#566566", relief=FLAT,
                          command=self.clear, padx=15, pady=5)
        btn_clear.pack(side=LEFT, padx=5)

        # ── Student Info Panel ─────────────────────────────────────────────
        info_frame = LabelFrame(body, text=" Student Information ", font=("Segoe UI", 12, "bold"),
                                bg="#F0F4F8", fg="#1A3E6F", bd=2, relief=GROOVE)
        info_frame.pack(fill=X, pady=(0, 15), ipady=10)

        # Student info display
        self.lbl_roll_val = Label(info_frame, text="--", font=("Segoe UI", 11, "bold"),
                                  bg="#E8F0FB", fg="#1A3E6F", relief=GROOVE, bd=2, width=15)
        self.lbl_roll_val.pack(side=LEFT, padx=(20, 10), pady=5)
        
        self.lbl_name_val = Label(info_frame, text="--", font=("Segoe UI", 11, "bold"),
                                  bg="#E8F0FB", fg="#1A3E6F", relief=GROOVE, bd=2, width=20)
        self.lbl_name_val.pack(side=LEFT, padx=10, pady=5)
        
        self.lbl_course_val = Label(info_frame, text="--", font=("Segoe UI", 11, "bold"),
                                    bg="#E8F0FB", fg="#1A3E6F", relief=GROOVE, bd=2, width=20)
        self.lbl_course_val.pack(side=LEFT, padx=10, pady=5)

        # ── Results Table ──────────────────────────────────────────────────
        table_frame = LabelFrame(body, text=" Subjects & Marks ", font=("Segoe UI", 12, "bold"),
                                 bg="#F0F4F8", fg="#1A3E6F", bd=2, relief=GROOVE)
        table_frame.pack(fill=BOTH, expand=True, pady=(0, 15))

        # Treeview
        cols = ("S.No", "Subject", "Marks Obtained", "Full Marks", "Percentage", "Grade")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=12)
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                        background="#1A3E6F", foreground="white")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=30)

        widths = [50, 350, 130, 110, 110, 80]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor=CENTER)
        
        # Column alignment for subject
        self.tree.column("Subject", anchor=W)

        # Tags for row colors
        self.tree.tag_configure("odd", background="#FFFFFF")
        self.tree.tag_configure("even", background="#EBF4FB")
        self.tree.tag_configure("fail", background="#FDE8E8")

        # Scrollbar
        scroll = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y)
        self.tree.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # ── Summary Panel ──────────────────────────────────────────────────
        summary_frame = Frame(body, bg="#F0F4F8")
        summary_frame.pack(fill=X, pady=(0, 10))
        
        self.lbl_summary = Label(summary_frame,
                                 text="Total: 0 / 0   |   Percentage: 0.00%   |   Grade: —   |   Result: —",
                                 font=("Segoe UI", 11, "bold"), bg="#1A3E6F", fg="white",
                                 relief=FLAT, anchor=CENTER, pady=8)
        self.lbl_summary.pack(fill=X)

        # ── Action Buttons ─────────────────────────────────────────────────
        btn_frame = Frame(body, bg="#F0F4F8")
        btn_frame.pack(fill=X)
        
        btn_delete = Button(btn_frame, text="🗑  Delete Selected Subject", 
                           font=("Segoe UI", 11, "bold"),
                           bg="#C0392B", fg="white", cursor="hand2",
                           activebackground="#922B21", relief=FLAT,
                           command=self.delete, padx=20, pady=8)
        btn_delete.pack(side=LEFT, padx=(0, 10))
        
        btn_delete_all = Button(btn_frame, text="⚠️  Delete All Subjects", 
                               font=("Segoe UI", 11, "bold"),
                               bg="#E67E22", fg="white", cursor="hand2",
                               activebackground="#B45F1B", relief=FLAT,
                               command=self.delete_all, padx=20, pady=8)
        btn_delete_all.pack(side=LEFT)

        # Store current student data
        self.current_roll = ""
        self.current_name = ""
        self.current_course = ""

    def _get_grade(self, percentage):
        """Calculate grade based on percentage"""
        if percentage >= 90:
            return "A+"
        elif percentage >= 80:
            return "A"
        elif percentage >= 70:
            return "B+"
        elif percentage >= 60:
            return "B"
        elif percentage >= 50:
            return "C"
        elif percentage >= 40:
            return "D"
        else:
            return "F"

    def _get_remark(self, percentage):
        """Get remark based on percentage"""
        if percentage >= 90:
            return "Outstanding"
        elif percentage >= 75:
            return "Distinction"
        elif percentage >= 60:
            return "First Division"
        elif percentage >= 50:
            return "Second Division"
        elif percentage >= 40:
            return "Pass"
        else:
            return "Fail"

    def search(self):
        """Search student and display all their subjects"""
        if self.var_search.get() == "":
            messagebox.showwarning("Input", "Please enter a roll number.", parent=self.root)
            return
            
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            roll_no = self.var_search.get()
            
            # Get student info
            cur.execute("SELECT name, course FROM student WHERE roll=?", (roll_no,))
            student = cur.fetchone()
            
            if student:
                self.current_roll = roll_no
                self.current_name = student[0]
                self.current_course = student[1]
                
                # Update student info display
                self.lbl_roll_val.config(text=roll_no)
                self.lbl_name_val.config(text=student[0])
                self.lbl_course_val.config(text=student[1])
                
                # Get all subjects for this student from result table
                cur.execute(""" 
                    SELECT course, marks_obtained, full_marks, percentage 
                    FROM result 
                    WHERE roll=? AND name=?
                    ORDER BY course
                """, (roll_no, student[0]))
                
                results = cur.fetchall()
                
                # Clear existing treeview items
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                if results:
                    total_obtained = 0
                    total_full = 0
                    
                    # Display each subject
                    for i, result in enumerate(results, 1):
                        subject = result[0]
                        marks_obtained = float(result[1])
                        full_marks = float(result[2])
                        percentage = float(result[3])
                        
                        # Calculate grade
                        grade = self._get_grade(percentage)
                        
                        # Determine tag for row color
                        tag = "fail" if percentage < 40 else ("even" if i % 2 == 0 else "odd")
                        
                        self.tree.insert("", END, values=(
                            i, subject, marks_obtained, full_marks, f"{percentage:.1f}%", grade
                        ), tags=(tag,))
                        
                        total_obtained += marks_obtained
                        total_full += full_marks
                    
                    # Calculate overall percentage
                    if total_full > 0:
                        overall_percentage = (total_obtained / total_full) * 100
                        overall_grade = self._get_grade(overall_percentage)
                        overall_remark = self._get_remark(overall_percentage)
                        
                        self.lbl_summary.config(
                            text=f"Total: {int(total_obtained)} / {int(total_full)}   |   "
                                 f"Percentage: {overall_percentage:.2f}%   |   "
                                 f"Grade: {overall_grade}   |   Result: {overall_remark}",
                            bg="#27AE60" if overall_percentage >= 40 else "#C0392B"
                        )
                    else:
                        self.lbl_summary.config(
                            text="Total: 0 / 0   |   Percentage: 0.00%   |   Grade: —   |   Result: —",
                            bg="#1A3E6F"
                        )
                    
                    messagebox.showinfo("Loaded", f"Found {len(results)} subject(s) for {student[0]}", 
                                       parent=self.root)
                else:
                    messagebox.showinfo("Info", f"No results found for Roll No: {roll_no}", 
                                       parent=self.root)
                    self.clear()
            else:
                messagebox.showerror("Error", f"Student with Roll No: {roll_no} not found", 
                                    parent=self.root)
                self.clear()
                    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        """Clear all displayed data"""
        self.var_search.set("")
        self.current_roll = ""
        self.current_name = ""
        self.current_course = ""
        
        # Clear student info
        self.lbl_roll_val.config(text="--")
        self.lbl_name_val.config(text="--")
        self.lbl_course_val.config(text="--")
        
        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Clear summary
        self.lbl_summary.config(
            text="Total: 0 / 0   |   Percentage: 0.00%   |   Grade: —   |   Result: —",
            bg="#1A3E6F"
        )

    def delete(self):
        """Delete selected subject result"""
        selected = self.tree.selection()
        
        if not selected:
            messagebox.showwarning("Warning", "Please select a subject to delete", parent=self.root)
            return
        
        if not self.current_roll:
            messagebox.showwarning("Warning", "Please search for a student first", parent=self.root)
            return
        
        try:
            # Get the selected item's values
            item_values = self.tree.item(selected[0])["values"]
            if not item_values:
                messagebox.showerror("Error", "Invalid selection", parent=self.root)
                return
            
            subject = item_values[1]
            
            # Confirm deletion
            op = messagebox.askyesno("Confirm", 
                                     f"Do you really want to delete the result for\n"
                                     f"Student: {self.current_name}\n"
                                     f"Subject: {subject}?",
                                     parent=self.root)
            
            if op:
                con = sqlite3.connect(database="rms.db")
                cur = con.cursor()
                
                # Delete the specific subject result
                cur.execute(""" 
                    DELETE FROM result 
                    WHERE roll=? AND name=? AND course=?
                """, (self.current_roll, self.current_name, subject))
                
                con.commit()
                con.close()
                
                messagebox.showinfo("Success", "Result deleted successfully", parent=self.root)
                
                # Refresh the search to show updated results
                self.var_search.set(self.current_roll)
                self.search()
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def delete_all(self):
        """Delete all subjects for current student"""
        if not self.current_roll:
            messagebox.showwarning("Warning", "Please search for a student first", parent=self.root)
            return
        
        # Get all subjects count
        subjects = self.tree.get_children()
        if not subjects:
            messagebox.showwarning("Warning", "No subjects found to delete", parent=self.root)
            return
        
        # Confirm deletion
        op = messagebox.askyesno("Confirm", 
                                 f"Do you really want to delete ALL results for\n"
                                 f"Student: {self.current_name}?\n\n"
                                 f"This will remove {len(subjects)} subject(s).",
                                 parent=self.root)
        
        if op:
            try:
                con = sqlite3.connect(database="rms.db")
                cur = con.cursor()
                
                # Delete all results for this student
                cur.execute(""" 
                    DELETE FROM result 
                    WHERE roll=? AND name=?
                """, (self.current_roll, self.current_name))
                
                con.commit()
                con.close()
                
                messagebox.showinfo("Success", f"All results for {self.current_name} deleted successfully", 
                                   parent=self.root)
                
                # Refresh the search to show updated results
                self.var_search.set(self.current_roll)
                self.search()
                
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = reportClass(root)
    root.mainloop()