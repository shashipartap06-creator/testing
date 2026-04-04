from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# ── Modern Light Theme Colors ─────────────────────────────────────────────────
BG          = "#F0F4F8"        # Main background
CARD_BG     = "#FFFFFF"        # Card background
FRAME_BG    = "#FFFFFF"        # Frame background
ACCENT      = "#2B6CB0"        # Primary blue
ACCENT2     = "#1A3E6F"        # Darker blue (title bar)
GREEN       = "#27AE60"        # Success green
ORANGE      = "#E8692A"        # Warning orange
RED         = "#C0392B"        # Error red
TEXT_PRIMARY= "#1E293B"        # Dark text
TEXT_SECONDARY = "#475569"     # Secondary text
BORDER_COLOR = "#E2E8F0"       # Border color
ENTRY_BG    = "#F8FAFC"        # Entry background

FONT_TITLE  = ("Segoe UI", 12, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)

class reportClass:
    def __init__(self, root):
        self.root = root
        self.root.title("SRMS — View Student Results")
        self.root.geometry("1350x750+50+50")
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
        title_bar.pack_propagate(False)
        Label(title_bar, text="📊  View Student Results",
              font=("Segoe UI", 18, "bold"), bg=ACCENT2, fg="white").pack(side=LEFT, padx=20, pady=10)

        # Main body
        body = Frame(self.root, bg=BG)
        body.pack(fill=BOTH, expand=True, padx=20, pady=15)

        # ── Top Panel - Search ──────────────────────────────────────────────────
        search_frame = LabelFrame(body, text=" Search Student ",
                                  font=("Segoe UI", 12, "bold"),
                                  bg=CARD_BG, fg=ACCENT2, bd=2, relief=GROOVE)
        search_frame.pack(fill=X, pady=(0, 15), ipady=8)

        Label(search_frame, text="Roll No:", font=FONT_TITLE,
              bg=CARD_BG, fg=TEXT_SECONDARY).pack(side=LEFT, padx=(15, 10))

        self.search_entry = Entry(search_frame, textvariable=self.var_search,
                                  font=FONT_BODY, bg=ENTRY_BG, fg=TEXT_PRIMARY,
                                  relief=SOLID, bd=1, width=25)
        self.search_entry.pack(side=LEFT, padx=5)
        self.search_entry.bind("<Return>", lambda e: self.search())

        btn_search = Button(search_frame, text="🔍 Search", font=FONT_TITLE,
                           bg=ACCENT, fg="white", cursor="hand2", relief=FLAT,
                           command=self.search, padx=20, pady=5)
        btn_search.pack(side=LEFT, padx=10)
        btn_search.bind("<Return>", lambda e: self.search())

        btn_refresh = Button(search_frame, text="🔄 Refresh", font=FONT_TITLE,
                            bg=GREEN, fg="white", cursor="hand2", relief=FLAT,
                            command=self.clear, padx=20, pady=5)
        btn_refresh.pack(side=LEFT, padx=5)
        btn_refresh.bind("<Return>", lambda e: self.clear())

        # ── Student Info Panel ──────────────────────────────────────────────────
        info_frame = LabelFrame(body, text=" Student Information ",
                                font=("Segoe UI", 12, "bold"),
                                bg=CARD_BG, fg=ACCENT2, bd=2, relief=GROOVE)
        info_frame.pack(fill=X, pady=(0, 15), ipady=10)

        info_container = Frame(info_frame, bg=CARD_BG)
        info_container.pack(pady=10)

        # Roll No
        Label(info_container, text="Roll No:", font=FONT_TITLE,
              bg=CARD_BG, fg=TEXT_SECONDARY).grid(row=0, column=0, padx=(20, 5), pady=5, sticky=W)
        self.lbl_roll_val = Label(info_container, text="--", font=FONT_TITLE,
                                  bg=ENTRY_BG, fg=TEXT_PRIMARY, relief=GROOVE, bd=1,
                                  width=15, pady=3)
        self.lbl_roll_val.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        # Name
        Label(info_container, text="Name:", font=FONT_TITLE,
              bg=CARD_BG, fg=TEXT_SECONDARY).grid(row=0, column=2, padx=(20, 5), pady=5, sticky=W)
        self.lbl_name_val = Label(info_container, text="--", font=FONT_TITLE,
                                  bg=ENTRY_BG, fg=TEXT_PRIMARY, relief=GROOVE, bd=1,
                                  width=25, pady=3)
        self.lbl_name_val.grid(row=0, column=3, padx=5, pady=5, sticky=W)

        # Course
        Label(info_container, text="Course:", font=FONT_TITLE,
              bg=CARD_BG, fg=TEXT_SECONDARY).grid(row=0, column=4, padx=(20, 5), pady=5, sticky=W)
        self.lbl_course_val = Label(info_container, text="--", font=FONT_TITLE,
                                    bg=ENTRY_BG, fg=TEXT_PRIMARY, relief=GROOVE, bd=1,
                                    width=20, pady=3)
        self.lbl_course_val.grid(row=0, column=5, padx=5, pady=5, sticky=W)

        # ── Results Table ───────────────────────────────────────────────────────
        table_frame = LabelFrame(body, text=" Subjects & Marks ",
                                 font=("Segoe UI", 12, "bold"),
                                 bg=CARD_BG, fg=ACCENT2, bd=2, relief=GROOVE)
        table_frame.pack(fill=BOTH, expand=True, pady=(0, 15))

        # Treeview
        cols = ("S.No", "Subject", "Marks Obtained", "Full Marks", "Percentage", "Grade")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                        background=ACCENT2, foreground="white")
        style.configure("Treeview", font=FONT_BODY, rowheight=28,
                        background=CARD_BG, foreground=TEXT_PRIMARY, fieldbackground=CARD_BG)
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

        # Row tags
        self.tree.tag_configure("odd", background="#F8FAFC")
        self.tree.tag_configure("even", background="#FFFFFF")
        self.tree.tag_configure("fail", background="#FEE2E2")

        # ── Summary Panel ───────────────────────────────────────────────────────
        summary_frame = Frame(body, bg=BG)
        summary_frame.pack(fill=X, pady=(0, 10))

        self.lbl_summary = Label(summary_frame,
                                 text="Total: 0 / 0   |   Percentage: 0.00%   |   Grade: —   |   Result: —",
                                 font=FONT_TITLE, bg=ACCENT2, fg="white",
                                 relief=FLAT, anchor=CENTER, pady=8)
        self.lbl_summary.pack(fill=X)

        # ── Action Buttons ──────────────────────────────────────────────────────
        btn_frame = Frame(body, bg=BG)
        btn_frame.pack(fill=X)

        btn_delete = Button(btn_frame, text="🗑 Delete Selected Subject",
                           font=FONT_TITLE, bg=RED, fg="white", cursor="hand2",
                           activebackground="#922B21", relief=FLAT,
                           command=self.delete, padx=20, pady=8)
        btn_delete.pack(side=LEFT, padx=(0, 10))
        btn_delete.bind("<Return>", lambda e: self.delete())

        btn_delete_all = Button(btn_frame, text="⚠️ Delete All Subjects",
                               font=FONT_TITLE, bg=ORANGE, fg="white", cursor="hand2",
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
        roll_no = self.var_search.get().strip()
        if not roll_no:
            messagebox.showwarning("Input", "Please enter a roll number.", parent=self.root)
            self.search_entry.focus()
            return

        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT name, course FROM student WHERE roll=?", (roll_no,))
            student = cur.fetchone()
            if student:
                self.current_roll = roll_no
                self.current_name = student[0]
                self.current_course = student[1]

                self.lbl_roll_val.config(text=roll_no)
                self.lbl_name_val.config(text=student[0])
                self.lbl_course_val.config(text=student[1])

                cur.execute("""SELECT course, marks_obtained, full_marks, percentage
                               FROM result WHERE roll=? AND name=?
                               ORDER BY course""", (roll_no, student[0]))
                results = cur.fetchall()

                # Clear table
                for item in self.tree.get_children():
                    self.tree.delete(item)

                if results:
                    total_obtained = 0
                    total_full = 0
                    for i, row in enumerate(results, 1):
                        subject = row[0]
                        marks_obtained = float(row[1])
                        full_marks = float(row[2])
                        percentage = float(row[3])
                        grade = self._get_grade(percentage)
                        tag = "fail" if percentage < 40 else ("even" if i % 2 == 0 else "odd")
                        self.tree.insert("", END, values=(i, subject, marks_obtained, full_marks,
                                                          f"{percentage:.1f}%", grade), tags=(tag,))
                        total_obtained += marks_obtained
                        total_full += full_marks

                    overall_pct = (total_obtained / total_full) * 100 if total_full > 0 else 0
                    overall_grade = self._get_grade(overall_pct)
                    overall_remark = self._get_remark(overall_pct)

                    self.lbl_summary.config(
                        text=f"Total: {int(total_obtained)} / {int(total_full)}   |   "
                             f"Percentage: {overall_pct:.2f}%   |   Grade: {overall_grade}   |   Result: {overall_remark}",
                        bg=GREEN if overall_pct >= 40 else RED
                    )
                else:
                    messagebox.showinfo("Info", f"No results found for Roll No: {roll_no}", parent=self.root)
                    self.clear()
            else:
                messagebox.showerror("Error", f"Student with Roll No: {roll_no} not found", parent=self.root)
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

        self.lbl_summary.config(text="Total: 0 / 0   |   Percentage: 0.00%   |   Grade: —   |   Result: —",
                                bg=ACCENT2)
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
            confirm = messagebox.askyesno("Confirm",
                                          f"Do you really want to delete the result for\n"
                                          f"Student: {self.current_name}\nSubject: {subject}?",
                                          parent=self.root)
            if confirm:
                con = sqlite3.connect(database="rms.db")
                cur = con.cursor()
                cur.execute("DELETE FROM result WHERE roll=? AND name=? AND course=?",
                            (self.current_roll, self.current_name, subject))
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
        confirm = messagebox.askyesno("Confirm",
                                      f"Do you really want to delete ALL results for\n"
                                      f"Student: {self.current_name}?\n\n"
                                      f"This will remove {len(subjects)} subject(s).",
                                      parent=self.root)
        if confirm:
            try:
                con = sqlite3.connect(database="rms.db")
                cur = con.cursor()
                cur.execute("DELETE FROM result WHERE roll=? AND name=?", (self.current_roll, self.current_name))
                con.commit()
                con.close()
                messagebox.showinfo("Success", f"All results for {self.current_name} deleted successfully", parent=self.root)
                self.var_search.set(self.current_roll)
                self.search()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root= Tk()
    root.tk.call('tk', 'scaling', 1.4)
    obj = reportClass(root)
    root.mainloop()