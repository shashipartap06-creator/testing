from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
from create_db import create_db
import os
from datetime import datetime

# ─── PDF generation (reportlab) ───────────────────────────────────────────────
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle, HRFlowable)
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    REPORTLAB_OK = True
except ImportError:
    REPORTLAB_OK = False


def grade_from_pct(pct):
    if pct >= 90: return "A+"
    elif pct >= 80: return "A"
    elif pct >= 70: return "B+"
    elif pct >= 60: return "B"
    elif pct >= 50: return "C"
    elif pct >= 40: return "D"
    else: return "F"

def remark_from_pct(pct):
    if pct >= 90: return "Outstanding"
    elif pct >= 75: return "Distinction"
    elif pct >= 60: return "First Division"
    elif pct >= 50: return "Second Division"
    elif pct >= 40: return "Pass"
    else: return "Fail"


def generate_result_pdf(student_info, subjects, save_path):
    """Generate an A4 result card PDF."""
    doc = SimpleDocTemplate(
        save_path, pagesize=A4,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=1.5*cm, bottomMargin=1.5*cm
    )

    # ── Styles ──────────────────────────────────────────────────────────────
    DARK  = colors.HexColor("#1A3E6F")
    MED   = colors.HexColor("#2B6CB0")
    LIGHT = colors.HexColor("#D9E8F5")
    ORANGE= colors.HexColor("#E8692A")
    GRAY  = colors.HexColor("#F5F7FA")
    WHITE = colors.white

    title_style = ParagraphStyle("title", fontSize=20, fontName="Helvetica-Bold",
                                  textColor=DARK, alignment=TA_CENTER, spaceAfter=6)
    sub_style   = ParagraphStyle("sub",   fontSize=11, fontName="Helvetica",
                                  textColor=MED,  alignment=TA_CENTER, spaceAfter=8)
    label_style = ParagraphStyle("lbl",   fontSize=9,  fontName="Helvetica-Bold",
                                  textColor=DARK)
    value_style = ParagraphStyle("val",   fontSize=9,  fontName="Helvetica",
                                  textColor=colors.HexColor("#333333"))
    head_style  = ParagraphStyle("hd",    fontSize=10, fontName="Helvetica-Bold",
                                  textColor=WHITE, alignment=TA_CENTER)
    cell_style  = ParagraphStyle("cl",    fontSize=9,  fontName="Helvetica",
                                  textColor=colors.HexColor("#222222"), alignment=TA_CENTER)
    grade_style = ParagraphStyle("gr",    fontSize=11, fontName="Helvetica-Bold",
                                  textColor=ORANGE, alignment=TA_CENTER)
    remark_style= ParagraphStyle("rm",    fontSize=12, fontName="Helvetica-Bold",
                                  textColor=DARK, alignment=TA_CENTER)
    footer_style= ParagraphStyle("ft",    fontSize=8,  fontName="Helvetica",
                                  textColor=colors.HexColor("#888888"), alignment=TA_CENTER)

    story = []

    # ── Header ───────────────────────────────────────────────────────────────
    story.append(Paragraph("A.S. COLLEGE, KHANNA", title_style))
    story.append(Paragraph("Department of Computer Applications", sub_style))
    story.append(Spacer(1, 0.2*cm))
    story.append(HRFlowable(width="100%", thickness=2, color=DARK, spaceAfter=8))
    
    # Result Card Title
    story.append(Paragraph("STUDENT RESULT CARD", ParagraphStyle(
        "rc", fontSize=15, fontName="Helvetica-Bold",
        textColor=WHITE, alignment=TA_CENTER,
        backColor=DARK, spaceAfter=12, spaceBefore=6,
        borderPadding=(8, 4, 8, 4)
    )))
    story.append(Spacer(1, 0.2*cm))

    # ── Student Info Table ───────────────────────────────────────────────────
    total_obtained = sum(s["obtained"] for s in subjects)
    total_full     = sum(s["full"] for s in subjects)
    overall_pct    = (total_obtained / total_full * 100) if total_full > 0 else 0
    overall_grade  = grade_from_pct(overall_pct)
    overall_remark = remark_from_pct(overall_pct)

    page_w = A4[0] - 3.6*cm
    info_data = [
        [Paragraph("Roll No.", label_style),  Paragraph(str(student_info["roll"]),   value_style),
         Paragraph("Name",     label_style),  Paragraph(student_info["name"],         value_style)],
        [Paragraph("Course",   label_style),  Paragraph(student_info["course"],       value_style),
         Paragraph("Date",     label_style),  Paragraph(datetime.now().strftime("%d-%m-%Y"), value_style)],
    ]
    info_table = Table(info_data, colWidths=[2.2*cm, 6*cm, 2.2*cm, 6*cm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), GRAY),
        ("BACKGROUND", (0,0), (0,-1), LIGHT),
        ("BACKGROUND", (2,0), (2,-1), LIGHT),
        ("BOX",        (0,0), (-1,-1), 0.5, MED),
        ("INNERGRID",  (0,0), (-1,-1), 0.3, colors.HexColor("#C0D4E8")),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.6*cm))

    # ── Marks Table ──────────────────────────────────────────────────────────
    col_w = [1.2*cm, 6.5*cm, 2.8*cm, 2.8*cm, 2.5*cm, 2.0*cm]
    marks_data = [[
        Paragraph("S.No.",         head_style),
        Paragraph("Subject",       head_style),
        Paragraph("Marks Obtained",head_style),
        Paragraph("Full Marks",    head_style),
        Paragraph("Percentage",    head_style),
        Paragraph("Grade",         head_style),
    ]]
    for i, s in enumerate(subjects):
        pct   = (s["obtained"] / s["full"] * 100) if s["full"] > 0 else 0
        grade = grade_from_pct(pct)
        marks_data.append([
            Paragraph(str(i+1),          cell_style),
            Paragraph(s["subject"],      ParagraphStyle("ls", fontSize=9, fontName="Helvetica",
                                                         textColor=colors.HexColor("#222222"), alignment=TA_LEFT)),
            Paragraph(str(s["obtained"]),cell_style),
            Paragraph(str(s["full"]),    cell_style),
            Paragraph(f"{pct:.1f}%",     cell_style),
            Paragraph(grade,             ParagraphStyle("gc", fontSize=9, fontName="Helvetica-Bold",
                                                         textColor=ORANGE, alignment=TA_CENTER)),
        ])

    # Total row
    marks_data.append([
        Paragraph("", cell_style),
        Paragraph("TOTAL", ParagraphStyle("tot", fontSize=10, fontName="Helvetica-Bold",
                                           textColor=DARK, alignment=TA_LEFT)),
        Paragraph(str(total_obtained), ParagraphStyle("tb", fontSize=10, fontName="Helvetica-Bold",
                                                        textColor=DARK, alignment=TA_CENTER)),
        Paragraph(str(total_full),     ParagraphStyle("tb2",fontSize=10, fontName="Helvetica-Bold",
                                                        textColor=DARK, alignment=TA_CENTER)),
        Paragraph(f"{overall_pct:.1f}%",ParagraphStyle("tp", fontSize=10, fontName="Helvetica-Bold",
                                                         textColor=DARK, alignment=TA_CENTER)),
        Paragraph(overall_grade,        ParagraphStyle("tg", fontSize=10, fontName="Helvetica-Bold",
                                                         textColor=ORANGE, alignment=TA_CENTER)),
    ])

    marks_table = Table(marks_data, colWidths=col_w)
    n = len(marks_data)
    marks_table.setStyle(TableStyle([
        # Header row
        ("BACKGROUND",    (0,0), (-1,0),  DARK),
        ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
        # Alternating rows
        *[("BACKGROUND", (0,r), (-1,r), GRAY if r%2==0 else WHITE) for r in range(1, n-1)],
        # Total row
        ("BACKGROUND",    (0,n-1),(-1,n-1), LIGHT),
        ("FONTNAME",      (0,n-1),(-1,n-1), "Helvetica-Bold"),
        # Grid
        ("BOX",           (0,0), (-1,-1), 1,   MED),
        ("INNERGRID",     (0,0), (-1,-1), 0.3, colors.HexColor("#C0D4E8")),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
        ("ALIGN",         (1,1), (1,n-1), "LEFT"),
    ]))
    story.append(marks_table)
    story.append(Spacer(1, 0.6*cm))

    # ── Result Summary Box ───────────────────────────────────────────────────
    summary_data = [[
        Paragraph("Overall Percentage", label_style),
        Paragraph(f"{overall_pct:.2f}%", grade_style),
        Paragraph("Grade", label_style),
        Paragraph(overall_grade, grade_style),
        Paragraph("Result", label_style),
        Paragraph(overall_remark, remark_style),
    ]]
    summary_table = Table(summary_data, colWidths=[3.5*cm, 3*cm, 2*cm, 2*cm, 2.5*cm, 4.4*cm])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), LIGHT),
        ("BOX",           (0,0), (-1,-1), 1.5, DARK),
        ("INNERGRID",     (0,0), (-1,-1), 0.5, MED),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.8*cm))

    # ── Grade Legend ─────────────────────────────────────────────────────────
    legend = [["Grade Scale:", "A+(≥90)", "A(≥80)", "B+(≥70)", "B(≥60)", "C(≥50)", "D(≥40)", "F(<40)"]]
    legend_table = Table(legend, colWidths=[2.5*cm]+[2.1*cm]*7)
    legend_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,0), DARK),
        ("BACKGROUND",    (1,0), (-1,0), GRAY),
        ("TEXTCOLOR",     (0,0), (0,0), WHITE),
        ("FONTNAME",      (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 8),
        ("BOX",           (0,0), (-1,-1), 0.5, MED),
        ("INNERGRID",     (0,0), (-1,-1), 0.3, MED),
        ("ALIGN",         (0,0), (-1,-1), "CENTER"),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(legend_table)
    story.append(Spacer(1, 1.2*cm))

    # ── Footer (only) ────────────────────────────────────────────────────────
    # Removed signature section as requested
    story.append(HRFlowable(width="100%", thickness=1, color=MED, spaceBefore=0, spaceAfter=4))
    story.append(Paragraph(
        f"Generated by Student Result Management System (SRMS)  |  A.S. College, Khanna  |  {datetime.now().strftime('%d %b %Y, %I:%M %p')}",
        footer_style
    ))

    doc.build(story)


# ─── Main Result Window ────────────────────────────────────────────────────────
class resultClass:
    def __init__(self, root):
        self.root = root
        self.root.title("STUDENT RESULT MANAGEMENT SYSTEM")
        self.root.geometry("1200x650+60+30")
        self.root.config(bg="#F0F4F8")
        self.root.focus_force()

        # ── Title Bar ──────────────────────────────────────────────────────
        title_bar = Frame(self.root, bg="#1A3E6F", height=55)
        title_bar.pack(fill=X, side=TOP)
        Label(title_bar, text="  📋  Add Student Results",
              font=("Segoe UI", 18, "bold"), bg="#1A3E6F", fg="white").pack(side=LEFT, pady=10, padx=15)

        # ── Main body ──────────────────────────────────────────────────────
        body = Frame(self.root, bg="#F0F4F8")
        body.pack(fill=BOTH, expand=True, padx=15, pady=12)

        # Left panel — student info
        left = LabelFrame(body, text=" Student Info ", font=("Segoe UI", 11, "bold"),
                          bg="#F0F4F8", fg="#1A3E6F", bd=2, relief=GROOVE)
        left.pack(side=LEFT, fill=Y, padx=(0, 10), pady=0, ipadx=10, ipady=8)

        self.var_roll   = StringVar()
        self.var_name   = StringVar()
        self.var_course = StringVar()
        self.roll_list  = []
        self._fetch_rolls()

        self._field(left, "Select Roll No.", 0)
        self.cmb_roll = ttk.Combobox(left, textvariable=self.var_roll, values=self.roll_list,
                                     font=("Segoe UI", 11), state="readonly", width=18)
        self.cmb_roll.grid(row=1, column=0, columnspan=2, padx=10, pady=(0,6), sticky=EW)
        self.cmb_roll.set("-- Select --")

        btn_search = Button(left, text="🔍 Search Student", font=("Segoe UI", 10, "bold"),
                            bg="#2B6CB0", fg="white", cursor="hand2",
                            activebackground="#1A3E6F", relief=FLAT,
                            command=self._search)
        btn_search.grid(row=2, column=0, columnspan=2, padx=10, pady=4, sticky=EW)

        self._field(left, "Name", 3)
        Entry(left, textvariable=self.var_name, font=("Segoe UI", 11),
              bg="#E8F0FB", state="readonly", relief=FLAT, bd=2
              ).grid(row=4, column=0, columnspan=2, padx=10, pady=(0,6), sticky=EW)

        self._field(left, "Course", 5)
        Entry(left, textvariable=self.var_course, font=("Segoe UI", 11),
              bg="#E8F0FB", state="readonly", relief=FLAT, bd=2
              ).grid(row=6, column=0, columnspan=2, padx=10, pady=(0,12), sticky=EW)

        # ── Subject entry ──────────────────────────────────────────────────
        subj_frame = LabelFrame(left, text=" Add Subject Marks ", font=("Segoe UI", 10, "bold"),
                                bg="#F0F4F8", fg="#1A3E6F", bd=2, relief=GROOVE)
        subj_frame.grid(row=7, column=0, columnspan=2, padx=8, pady=4, sticky=EW)

        self.var_subject  = StringVar()
        self.var_obtained = StringVar()
        self.var_full     = StringVar()

        Label(subj_frame, text="Subject Name", font=("Segoe UI", 9, "bold"),
              bg="#F0F4F8", fg="#333").grid(row=0, column=0, padx=8, pady=4, sticky=W)
        Entry(subj_frame, textvariable=self.var_subject, font=("Segoe UI", 10),
              bg="white", relief=SOLID, bd=1, width=18
              ).grid(row=1, column=0, padx=8, pady=(0,6), sticky=EW)

        Label(subj_frame, text="Marks Obtained", font=("Segoe UI", 9, "bold"),
              bg="#F0F4F8", fg="#333").grid(row=2, column=0, padx=8, pady=4, sticky=W)
        Entry(subj_frame, textvariable=self.var_obtained, font=("Segoe UI", 10),
              bg="white", relief=SOLID, bd=1, width=10
              ).grid(row=3, column=0, padx=8, pady=(0,6), sticky=EW)

        Label(subj_frame, text="Full Marks", font=("Segoe UI", 9, "bold"),
              bg="#F0F4F8", fg="#333").grid(row=4, column=0, padx=8, pady=4, sticky=W)
        Entry(subj_frame, textvariable=self.var_full, font=("Segoe UI", 10),
              bg="white", relief=SOLID, bd=1, width=10
              ).grid(row=5, column=0, padx=8, pady=(0,8), sticky=EW)

        btn_add_subj = Button(subj_frame, text="➕  Add Subject", font=("Segoe UI", 10, "bold"),
                              bg="#27AE60", fg="white", cursor="hand2",
                              activebackground="#1E8449", relief=FLAT,
                              command=self._add_subject)
        btn_add_subj.grid(row=6, column=0, padx=8, pady=4, sticky=EW)

        # Action buttons
        btn_frame = Frame(left, bg="#F0F4F8")
        btn_frame.grid(row=8, column=0, columnspan=2, padx=8, pady=10, sticky=EW)

        Button(btn_frame, text="💾 Save All",     font=("Segoe UI", 10, "bold"),
               bg="#1A3E6F", fg="white", cursor="hand2", relief=FLAT,
               activebackground="#0F2952", command=self._save_all
               ).pack(side=LEFT, fill=X, expand=True, padx=(0,4))

        Button(btn_frame, text="🗑 Remove Row",   font=("Segoe UI", 10, "bold"),
               bg="#C0392B", fg="white", cursor="hand2", relief=FLAT,
               activebackground="#922B21", command=self._remove_row
               ).pack(side=LEFT, fill=X, expand=True, padx=(0,4))

        Button(btn_frame, text="✖ Clear",         font=("Segoe UI", 10, "bold"),
               bg="#7F8C8D", fg="white", cursor="hand2", relief=FLAT,
               activebackground="#566566", command=self._clear
               ).pack(side=LEFT, fill=X, expand=True)

        # Right panel — subject table + PDF
        right = Frame(body, bg="#F0F4F8")
        right.pack(side=LEFT, fill=BOTH, expand=True)

        table_frame = LabelFrame(right, text=" Subjects & Marks ", font=("Segoe UI", 11, "bold"),
                                 bg="#F0F4F8", fg="#1A3E6F", bd=2, relief=GROOVE)
        table_frame.pack(fill=BOTH, expand=True, pady=(0,10))

        # Treeview
        cols = ("S.No", "Subject", "Marks Obtained", "Full Marks", "Percentage", "Grade")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                         background="#1A3E6F", foreground="white")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)

        widths = [50, 280, 130, 110, 110, 80]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor=CENTER)

        self.tree.tag_configure("odd",  background="#FFFFFF")
        self.tree.tag_configure("even", background="#EBF4FB")
        self.tree.tag_configure("fail", background="#FDE8E8")

        scroll = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y)
        self.tree.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Summary bar
        self.lbl_summary = Label(right,
                                  text="Total: 0 / 0   |   Percentage: 0.00%   |   Grade: —   |   Result: —",
                                  font=("Segoe UI", 11, "bold"), bg="#1A3E6F", fg="white",
                                  relief=FLAT, anchor=CENTER, pady=6)
        self.lbl_summary.pack(fill=X, pady=(0, 8))

        # PDF button
        Button(right, text="📄  Generate PDF Result Card",
               font=("Segoe UI", 12, "bold"), bg="#E8692A", fg="white",
               cursor="hand2", relief=FLAT, activebackground="#C0541F",
               command=self._generate_pdf, pady=8
               ).pack(fill=X)

        self.subjects = []   # list of dicts: {subject, obtained, full}

    # ── Helpers ────────────────────────────────────────────────────────────
    def _field(self, parent, text, row):
        Label(parent, text=text, font=("Segoe UI", 9, "bold"),
              bg="#F0F4F8", fg="#444").grid(row=row, column=0, padx=10, pady=(6,0), sticky=W)

    def _fetch_rolls(self):
        try:
            con = sqlite3.connect("rms.db")
            cur = con.cursor()
            cur.execute("select roll from student")
            for r in cur.fetchall():
                self.roll_list.append(r[0])
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _search(self):
        """Search student and load their existing subjects from database"""
        if self.var_roll.get() in ("", "-- Select --"):
            messagebox.showwarning("Input", "Please select a roll number.", parent=self.root)
            return
        try:
            con = sqlite3.connect("rms.db")
            cur = con.cursor()
            cur.execute("select name, course from student where roll=?", (self.var_roll.get(),))
            row = cur.fetchone()
            
            if row:
                self.var_name.set(row[0])
                self.var_course.set(row[1])
                
                # Load existing subjects for this student from result table
                # Note: In result table, 'course' column stores the subject name
                cur.execute(""" 
                    SELECT course, marks_obtained, full_marks 
                    FROM result 
                    WHERE roll=? AND name=?
                """, (self.var_roll.get(), row[0]))
                
                results = cur.fetchall()
                
                # Clear existing subjects and load from database
                self.subjects.clear()
                for result in results:
                    subject_name = result[0]  # This is the subject name
                    obtained = float(result[1])
                    full = float(result[2])
                    self.subjects.append({
                        "subject": subject_name, 
                        "obtained": obtained, 
                        "full": full
                    })
                
                # Refresh the treeview to show loaded subjects
                self._refresh_tree()
                
                con.close()
                
                # Show message if subjects were loaded
                if self.subjects:
                    messagebox.showinfo("Loaded", f"Loaded {len(self.subjects)} existing subject(s).", parent=self.root)
            else:
                messagebox.showerror("Not Found", "No student with that roll number.", parent=self.root)
                con.close()
                
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _add_subject(self):
        subj = self.var_subject.get().strip()
        obt  = self.var_obtained.get().strip()
        full = self.var_full.get().strip()

        if not subj:
            messagebox.showwarning("Input", "Subject name is required.", parent=self.root); return
        if self.var_name.get() == "":
            messagebox.showwarning("Input", "Please search a student first.", parent=self.root); return
        try:
            obt_f  = float(obt)
            full_f = float(full)
        except ValueError:
            messagebox.showerror("Error", "Marks must be numeric.", parent=self.root); return
        if obt_f > full_f:
            messagebox.showerror("Error", "Marks obtained cannot exceed full marks.", parent=self.root); return
        if full_f <= 0:
            messagebox.showerror("Error", "Full marks must be greater than 0.", parent=self.root); return

        # Duplicate subject check
        if any(s["subject"].lower() == subj.lower() for s in self.subjects):
            messagebox.showwarning("Duplicate", f"'{subj}' is already added.", parent=self.root); return

        self.subjects.append({"subject": subj, "obtained": obt_f, "full": full_f})
        self._refresh_tree()
        self.var_subject.set("")
        self.var_obtained.set("")
        self.var_full.set("")

    def _refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        total_obt  = 0
        total_full = 0
        for i, s in enumerate(self.subjects):
            pct   = (s["obtained"] / s["full"] * 100) if s["full"] > 0 else 0
            grade = grade_from_pct(pct)
            tag   = ("fail" if pct < 40 else ("even" if i % 2 == 0 else "odd"))
            self.tree.insert("", END,
                             values=(i+1, s["subject"],
                                     int(s["obtained"]) if s["obtained"].is_integer() else s["obtained"],
                                     int(s["full"])     if s["full"].is_integer()     else s["full"],
                                     f"{pct:.1f}%", grade),
                             tags=(tag,))
            total_obt  += s["obtained"]
            total_full += s["full"]

        if total_full > 0:
            overall = total_obt / total_full * 100
            grade   = grade_from_pct(overall)
            remark  = remark_from_pct(overall)
            self.lbl_summary.config(
                text=f"Total: {int(total_obt)} / {int(total_full)}   |   "
                     f"Percentage: {overall:.2f}%   |   Grade: {grade}   |   Result: {remark}",
                bg="#27AE60" if overall >= 40 else "#C0392B"
            )
        else:
            self.lbl_summary.config(
                text="Total: 0 / 0   |   Percentage: 0.00%   |   Grade: —   |   Result: —",
                bg="#1A3E6F"
            )

    def _remove_row(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select", "Click a subject row to remove.", parent=self.root); return
        idx = int(self.tree.item(selected[0])["values"][0]) - 1
        self.subjects.pop(idx)
        self._refresh_tree()

    def _clear(self):
        self.var_roll.set("-- Select --")
        self.var_name.set("")
        self.var_course.set("")
        self.var_subject.set("")
        self.var_obtained.set("")
        self.var_full.set("")
        self.subjects.clear()
        self._refresh_tree()

    def _save_all(self):
        """Save all subjects to database, skipping duplicates"""
        if not self.var_name.get():
            messagebox.showwarning("Input", "Please search a student first.", parent=self.root)
            return
        if not self.subjects:
            messagebox.showwarning("Input", "Add at least one subject.", parent=self.root)
            return
        try:
            con = sqlite3.connect("rms.db")
            cur = con.cursor()
            saved = 0
            skipped = 0
            
            for s in self.subjects:
                # Check if this subject already exists for this student
                # Note: Using 'course' column to check for subject name
                cur.execute(""" 
                    SELECT * FROM result 
                    WHERE roll=? AND name=? AND course=?
                """, (self.var_roll.get(), self.var_name.get(), s["subject"]))
                
                if cur.fetchone():
                    skipped += 1
                    continue
                
                pct = (s["obtained"] / s["full"] * 100) if s["full"] > 0 else 0
                
                # Insert new result
                cur.execute(
                    """INSERT INTO result(roll, name, course, marks_obtained, full_marks, percentage) 
                       VALUES(?, ?, ?, ?, ?, ?)""",
                    (self.var_roll.get(), 
                     self.var_name.get(),
                     s["subject"],           # Subject name goes in 'course' column
                     str(s["obtained"]), 
                     str(s["full"]), 
                     f"{pct:.2f}")
                )
                saved += 1
                
            con.commit()
            con.close()
            
            msg = f"{saved} result(s) saved successfully."
            if skipped:
                msg += f"\n{skipped} subject(s) already existed and were skipped."
            messagebox.showinfo("Saved", msg, parent=self.root)
            
            # Refresh the treeview to show any changes
            self._refresh_tree()
            
        except Exception as ex:
            messagebox.showerror("Error", str(ex), parent=self.root)

    def _generate_pdf(self):
        if not self.var_name.get():
            messagebox.showwarning("Input", "Please search a student first.", parent=self.root)
            return
        if not self.subjects:
            messagebox.showwarning("Input", "Add at least one subject before generating PDF.", parent=self.root)
            return
        if not REPORTLAB_OK:
            messagebox.showerror("Missing Library",
                                  "reportlab is not installed.\nRun: pip install reportlab",
                                  parent=self.root)
            return
        student_info = {
            "roll":   self.var_roll.get(),
            "name":   self.var_name.get(),
            "course": self.var_course.get(),
        }
        filename = f"Result_{self.var_roll.get()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        save_path = os.path.join(os.getcwd(), filename)
        try:
            generate_result_pdf(student_info, self.subjects, save_path)
            messagebox.showinfo("PDF Generated",
                                 f"Result card saved as:\n{filename}\n\nOpening PDF...",
                                 parent=self.root)
            os.startfile(save_path) if os.name == "nt" else os.system(f"xdg-open '{save_path}'")
        except Exception as ex:
            messagebox.showerror("PDF Error", str(ex), parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = resultClass(root)
    root.mainloop()