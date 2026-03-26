from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from create_db import create_db
from result import resultClass
from datetime import datetime

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
LIGHT_BG  = "#2A3A4A"  # Lighter background for display fields
DARK_TEXT = "#FFFFFF"  # White text for better contrast

FONT_TITLE  = ("Segoe UI", 11, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)

class reportClass:
    def __init__(self, root):
        self.root = root
        self.root.title("SRMS — View Student Results")
        self.root.geometry("1500x750+30+30")
        self.root.config(bg=BG)
        self.root.focus_force()

        # Variables
        self.var_search = StringVar()
        self.current_roll = ""
        self.current_name = ""
        self.current_course = ""

        # Build UI
        self._build_layout()

    def _build_layout(self):
        # Title Bar
        title_bar = Frame(self.root, bg=ACCENT2, height=55)
        title_bar.pack(fill=X, side=TOP)
        Label(title_bar, text="  📊  View Student Results",
              font=("Segoe UI", 18, "bold"), bg=ACCENT2, fg=WHITE).pack(side=LEFT, pady=10, padx=15)

        # Main body
        body = Frame(self.root, bg=BG)
        body.pack(fill=BOTH, expand=True, padx=20, pady=15)

        # ── Top Panel - Search ──────────────────────────────────────────────────
        search_frame = Frame(body, bg=CARD_BG, height=70)
        search_frame.pack(fill=X, pady=(0, 15))
        search_frame.pack_propagate(False)
        
        Label(search_frame, text="🔍 Search by Roll No:", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).pack(side=LEFT, padx=(20, 10), pady=20)
        
        self.search_entry = Entry(search_frame, textvariable=self.var_search,
                                   font=FONT_BODY, bg=LIGHT_BG, fg=WHITE, 
                                   relief=SOLID, bd=1, width=25,
                                   insertbackground=WHITE)
        self.search_entry.pack(side=LEFT, padx=5, pady=20)
        self.search_entry.bind("<Return>", lambda e: self.search())
        
        btn_search = Button(search_frame, text="Search", font=FONT_TITLE,
                           bg=ACCENT, fg=WHITE, cursor="hand2", relief=FLAT,
                           command=self.search, padx=25, pady=5)
        btn_search.pack(side=LEFT, padx=10, pady=20)
        btn_search.bind("<Return>", lambda e: self.search())
        
        btn_refresh = Button(search_frame, text="Refresh", font=FONT_TITLE,
                            bg=GREEN, fg=WHITE, cursor="hand2", relief=FLAT,
                            command=self.clear, padx=25, pady=5)
        btn_refresh.pack(side=LEFT, padx=5, pady=20)
        btn_refresh.bind("<Return>", lambda e: self.clear())

        # ── Student Info Panel ──────────────────────────────────────────────────
        info_frame = LabelFrame(body, text=" Student Information ", font=FONT_TITLE,
                                bg=CARD_BG, fg=TEXT, bd=2, relief=GROOVE)
        info_frame.pack(fill=X, pady=(0, 15), ipady=10)
        
        info_container = Frame(info_frame, bg=CARD_BG)
        info_container.pack(pady=10)
        
        # Roll No
        Label(info_container, text="Roll No:", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).grid(row=0, column=0, padx=(20, 5), pady=5, sticky=W)
        self.lbl_roll_val = Label(info_container, text="--", font=FONT_TITLE,
                                  bg=LIGHT_BG, fg=WHITE, relief=GROOVE, bd=1, width=15, pady=3)
        self.lbl_roll_val.grid(row=0, column=1, padx=5, pady=5, sticky=W)
        
        # Name
        Label(info_container, text="Name:", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).grid(row=0, column=2, padx=(20, 5), pady=5, sticky=W)
        self.lbl_name_val = Label(info_container, text="--", font=FONT_TITLE,
                                  bg=LIGHT_BG, fg=WHITE, relief=GROOVE, bd=1, width=25, pady=3)
        self.lbl_name_val.grid(row=0, column=3, padx=5, pady=5, sticky=W)
        
        # Course
        Label(info_container, text="Course:", font=FONT_TITLE,
              bg=CARD_BG, fg=SUBTEXT).grid(row=0, column=4, padx=(20, 5), pady=5, sticky=W)
        self.lbl_course_val = Label(info_container, text="--", font=FONT_TITLE,
                                    bg=LIGHT_BG, fg=WHITE, relief=GROOVE, bd=1, width=20, pady=3)
        self.lbl_course_val.grid(row=0, column=5, padx=5, pady=5, sticky=W)

        # ── Results Table ───────────────────────────────────────────────────────
        table_frame = LabelFrame(body, text=" Subjects & Marks ", font=FONT_TITLE,
                                 bg=CARD_BG, fg=TEXT, bd=2, relief=GROOVE)
        table_frame.pack(fill=BOTH, expand=True, pady=(0, 15))

        # Treeview
        cols = ("S.No", "Subject", "Marks Obtained", "Full Marks", "Percentage", "Grade")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                        background=ACCENT2, foreground=WHITE)
        style.configure("Treeview", font=FONT_BODY, rowheight=28,
                        background=CARD_BG, foreground=TEXT, fieldbackground=CARD_BG)
        style.map('Treeview', background=[('selected', ACCENT)])

        widths = [50, 350, 130, 110, 110, 80]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor=CENTER)
        self.tree.column("Subject", anchor=W)

        scroll = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y)
        self.tree.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        self.tree.tag_configure("odd", background="#1E2E42")
        self.tree.tag_configure("even", background="#162032")
        self.tree.tag_configure("fail", background="#5a2a2a")

        # ── Summary Panel ───────────────────────────────────────────────────────
        summary_frame = Frame(body, bg=BG)
        summary_frame.pack(fill=X, pady=(0, 10))
        
        self.lbl_summary = Label(summary_frame,
                                 text="Total: 0 / 0   |   Percentage: 0.00%   |   Grade: —   |   Result: —",
                                 font=FONT_TITLE, bg=ACCENT2, fg=WHITE,
                                 relief=FLAT, anchor=CENTER, pady=8)
        self.lbl_summary.pack(fill=X)

        # ── Action Buttons ──────────────────────────────────────────────────────
        btn_frame = Frame(body, bg=BG)
        btn_frame.pack(fill=X)
        
        btn_delete = Button(btn_frame, text="🗑 Delete Selected Subject", 
                           font=FONT_TITLE, bg="#C0392B", fg=WHITE, cursor="hand2",
                           activebackground="#922B21", relief=FLAT,
                           command=self.delete, padx=20, pady=8)
        btn_delete.pack(side=LEFT, padx=(0, 10))
        btn_delete.bind("<Return>", lambda e: self.delete())
        
        btn_delete_all = Button(btn_frame, text="⚠️ Delete All Subjects", 
                               font=FONT_TITLE, bg="#E67E22", fg=WHITE, cursor="hand2",
                               activebackground="#B45F1B", relief=FLAT,
                               command=self.delete_all, padx=20, pady=8)
        btn_delete_all.pack(side=LEFT)
        btn_delete_all.bind("<Return>", lambda e: self.delete_all())

    def _get_grade(self, percentage):
        if percentage >= 90: return "A+"
        elif percentage >= 80: return "A"
        elif percentage >= 70: return "B+"
        elif percentage >= 60: return "B"
        elif percentage >= 50: return "C"
        elif percentage >= 40: return "D"
        else: return "F"

    def _get_remark(self, percentage):
        if percentage >= 90: return "Outstanding"
        elif percentage >= 75: return "Distinction"
        elif percentage >= 60: return "First Division"
        elif percentage >= 50: return "Second Division"
        elif percentage >= 40: return "Pass"
        else: return "Fail"

    def search(self):
        if self.var_search.get() == "":
            messagebox.showwarning("Input", "Please enter a roll number.", parent=self.root)
            self.search_entry.focus()
            return
            
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            roll_no = self.var_search.get()
            
            cur.execute("SELECT name, course FROM student WHERE roll=?", (roll_no,))
            student = cur.fetchone()
            
            if student:
                self.current_roll = roll_no
                self.current_name = student[0]
                self.current_course = student[1]
                
                self.lbl_roll_val.config(text=roll_no)
                self.lbl_name_val.config(text=student[0])
                self.lbl_course_val.config(text=student[1])
                
                cur.execute(""" 
                    SELECT course, marks_obtained, full_marks, percentage 
                    FROM result 
                    WHERE roll=? AND name=?
                    ORDER BY course
                """, (roll_no, student[0]))
                
                results = cur.fetchall()
                
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                if results:
                    total_obtained = 0
                    total_full = 0
                    
                    for i, result in enumerate(results, 1):
                        subject = result[0]
                        marks_obtained = float(result[1])
                        full_marks = float(result[2])
                        percentage = float(result[3])
                        grade = self._get_grade(percentage)
                        
                        tag = "fail" if percentage < 40 else ("even" if i % 2 == 0 else "odd")
                        
                        self.tree.insert("", END, values=(
                            i, subject, marks_obtained, full_marks, f"{percentage:.1f}%", grade
                        ), tags=(tag,))
                        
                        total_obtained += marks_obtained
                        total_full += full_marks
                    
                    if total_full > 0:
                        overall_percentage = (total_obtained / total_full) * 100
                        overall_grade = self._get_grade(overall_percentage)
                        overall_remark = self._get_remark(overall_percentage)
                        
                        self.lbl_summary.config(
                            text=f"Total: {int(total_obtained)} / {int(total_full)}   |   "
                                 f"Percentage: {overall_percentage:.2f}%   |   "
                                 f"Grade: {overall_grade}   |   Result: {overall_remark}",
                            bg=GREEN if overall_percentage >= 40 else "#C0392B"
                        )
                    else:
                        self.lbl_summary.config(
                            text="Total: 0 / 0   |   Percentage: 0.00%   |   Grade: —   |   Result: —",
                            bg=ACCENT2
                        )
                else:
                    messagebox.showinfo("Info", f"No results found for Roll No: {roll_no}", 
                                       parent=self.root)
            else:
                messagebox.showerror("Error", f"Student with Roll No: {roll_no} not found", 
                                    parent=self.root)
                self.clear()
                    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_search.set("")
        self.current_roll = ""
        self.current_name = ""
        self.current_course = ""
        
        self.lbl_roll_val.config(text="--")
        self.lbl_name_val.config(text="--")
        self.lbl_course_val.config(text="--")
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.lbl_summary.config(
            text="Total: 0 / 0   |   Percentage: 0.00%   |   Grade: —   |   Result: —",
            bg=ACCENT2
        )
        self.search_entry.focus()

    def delete(self):
        selected = self.tree.selection()
        
        if not selected:
            messagebox.showwarning("Warning", "Please select a subject to delete", parent=self.root)
            return
        
        if not self.current_roll:
            messagebox.showwarning("Warning", "Please search for a student first", parent=self.root)
            return
        
        try:
            item_values = self.tree.item(selected[0])["values"]
            if not item_values:
                messagebox.showerror("Error", "Invalid selection", parent=self.root)
                return
            
            subject = item_values[1]
            
            op = messagebox.askyesno("Confirm", 
                                     f"Do you really want to delete the result for\n"
                                     f"Student: {self.current_name}\n"
                                     f"Subject: {subject}?",
                                     parent=self.root)
            
            if op:
                con = sqlite3.connect(database="rms.db")
                cur = con.cursor()
                
                cur.execute(""" 
                    DELETE FROM result 
                    WHERE roll=? AND name=? AND course=?
                """, (self.current_roll, self.current_name, subject))
                
                con.commit()
                con.close()
                
                messagebox.showinfo("Success", "Result deleted successfully", parent=self.root)
                
                self.var_search.set(self.current_roll)
                self.search()
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def delete_all(self):
        if not self.current_roll:
            messagebox.showwarning("Warning", "Please search for a student first", parent=self.root)
            return
        
        subjects = self.tree.get_children()
        if not subjects:
            messagebox.showwarning("Warning", "No subjects found to delete", parent=self.root)
            return
        
        op = messagebox.askyesno("Confirm", 
                                 f"Do you really want to delete ALL results for\n"
                                 f"Student: {self.current_name}?\n\n"
                                 f"This will remove {len(subjects)} subject(s).",
                                 parent=self.root)
        
        if op:
            try:
                con = sqlite3.connect(database="rms.db")
                cur = con.cursor()
                
                cur.execute(""" 
                    DELETE FROM result 
                    WHERE roll=? AND name=?
                """, (self.current_roll, self.current_name))
                
                con.commit()
                con.close()
                
                messagebox.showinfo("Success", f"All results for {self.current_name} deleted successfully", 
                                   parent=self.root)
                
                self.var_search.set(self.current_roll)
                self.search()
                
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = reportClass(root)
    root.mainloop()