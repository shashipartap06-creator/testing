from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import os
from datetime import datetime

# ── Modern Light Theme Colors ─────────────────────────────────────────────────
BG          = "#F0F4F8"
CARD_BG     = "#FFFFFF"
ACCENT      = "#2B6CB0"
ACCENT2     = "#1A3E6F"
GREEN       = "#27AE60"
ORANGE      = "#E8692A"
RED         = "#C0392B"
TEXT_PRIMARY = "#1E293B"
TEXT_SECONDARY = "#475569"
BORDER_COLOR = "#E2E8F0"
ENTRY_BG    = "#F8FAFC"

FONT_TITLE  = ("Segoe UI", 12, "bold")
FONT_BODY   = ("Segoe UI", 10)

# ─── PDF generation (reportlab) ───────────────────────────────────────────────
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
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
    doc = SimpleDocTemplate(save_path, pagesize=A4,
                            leftMargin=1.8*cm, rightMargin=1.8*cm,
                            topMargin=1.5*cm, bottomMargin=1.5*cm)
    DARK = colors.HexColor("#1A3E6F")
    MED = colors.HexColor("#2B6CB0")
    LIGHT = colors.HexColor("#D9E8F5")
    ORANGE_COL = colors.HexColor("#E8692A")
    GRAY = colors.HexColor("#F5F7FA")
    WHITE = colors.white

    title_style = ParagraphStyle("title", fontSize=20, fontName="Helvetica-Bold",
                                 textColor=DARK, alignment=TA_CENTER, spaceAfter=6)
    sub_style = ParagraphStyle("sub", fontSize=11, fontName="Helvetica",
                               textColor=MED, alignment=TA_CENTER, spaceAfter=8)
    label_style = ParagraphStyle("lbl", fontSize=9, fontName="Helvetica-Bold",
                                 textColor=DARK)
    value_style = ParagraphStyle("val", fontSize=9, fontName="Helvetica",
                                 textColor=colors.HexColor("#333333"))
    head_style = ParagraphStyle("hd", fontSize=10, fontName="Helvetica-Bold",
                                textColor=WHITE, alignment=TA_CENTER)
    cell_style = ParagraphStyle("cl", fontSize=9, fontName="Helvetica",
                                textColor=colors.HexColor("#222222"), alignment=TA_CENTER)
    grade_style = ParagraphStyle("gr", fontSize=11, fontName="Helvetica-Bold",
                                 textColor=ORANGE_COL, alignment=TA_CENTER)
    remark_style = ParagraphStyle("rm", fontSize=12, fontName="Helvetica-Bold",
                                  textColor=DARK, alignment=TA_CENTER)
    footer_style = ParagraphStyle("ft", fontSize=8, fontName="Helvetica",
                                  textColor=colors.HexColor("#888888"), alignment=TA_CENTER)

    story = []
    story.append(Paragraph("A.S. COLLEGE, KHANNA", title_style))
    story.append(Paragraph("Department of Computer Applications", sub_style))
    story.append(Spacer(1, 0.2*cm))
    story.append(HRFlowable(width="100%", thickness=2, color=DARK, spaceAfter=8))
    story.append(Paragraph("STUDENT RESULT CARD", ParagraphStyle(
        "rc", fontSize=15, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER,
        backColor=DARK, spaceAfter=12, spaceBefore=6, borderPadding=(8,4,8,4))))
    story.append(Spacer(1, 0.2*cm))

    total_obtained = sum(s["obtained"] for s in subjects)
    total_full = sum(s["full"] for s in subjects)
    overall_pct = (total_obtained / total_full * 100) if total_full > 0 else 0
    overall_grade = grade_from_pct(overall_pct)
    overall_remark = remark_from_pct(overall_pct)

    info_data = [
        [Paragraph("Roll No.", label_style), Paragraph(str(student_info["roll"]), value_style),
         Paragraph("Name", label_style), Paragraph(student_info["name"], value_style)],
        [Paragraph("Course", label_style), Paragraph(student_info["course"], value_style),
         Paragraph("Date", label_style), Paragraph(datetime.now().strftime("%d-%m-%Y"), value_style)],
    ]
    info_table = Table(info_data, colWidths=[2.2*cm, 6*cm, 2.2*cm, 6*cm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), GRAY), ("BACKGROUND", (0,0), (0,-1), LIGHT),
        ("BACKGROUND", (2,0), (2,-1), LIGHT), ("BOX", (0,0), (-1,-1), 0.5, MED),
        ("INNERGRID", (0,0), (-1,-1), 0.3, colors.HexColor("#C0D4E8")),
        ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 8), ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.6*cm))

    col_w = [1.2*cm, 6.5*cm, 2.8*cm, 2.8*cm, 2.5*cm, 2.0*cm]
    marks_data = [[Paragraph("S.No.", head_style), Paragraph("Subject", head_style),
                   Paragraph("Marks Obtained", head_style), Paragraph("Full Marks", head_style),
                   Paragraph("Percentage", head_style), Paragraph("Grade", head_style)]]
    for i, s in enumerate(subjects):
        pct = (s["obtained"] / s["full"] * 100) if s["full"] > 0 else 0
        grade = grade_from_pct(pct)
        marks_data.append([
            Paragraph(str(i+1), cell_style),
            Paragraph(s["subject"], ParagraphStyle("ls", fontSize=9, fontName="Helvetica",
                                                   textColor=colors.HexColor("#222222"), alignment=TA_LEFT)),
            Paragraph(str(s["obtained"]), cell_style),
            Paragraph(str(s["full"]), cell_style),
            Paragraph(f"{pct:.1f}%", cell_style),
            Paragraph(grade, ParagraphStyle("gc", fontSize=9, fontName="Helvetica-Bold",
                                            textColor=ORANGE_COL, alignment=TA_CENTER)),
        ])
    marks_data.append([
        Paragraph("", cell_style),
        Paragraph("TOTAL", ParagraphStyle("tot", fontSize=10, fontName="Helvetica-Bold", textColor=DARK, alignment=TA_LEFT)),
        Paragraph(str(total_obtained), ParagraphStyle("tb", fontSize=10, fontName="Helvetica-Bold", textColor=DARK, alignment=TA_CENTER)),
        Paragraph(str(total_full), ParagraphStyle("tb2", fontSize=10, fontName="Helvetica-Bold", textColor=DARK, alignment=TA_CENTER)),
        Paragraph(f"{overall_pct:.1f}%", ParagraphStyle("tp", fontSize=10, fontName="Helvetica-Bold", textColor=DARK, alignment=TA_CENTER)),
        Paragraph(overall_grade, ParagraphStyle("tg", fontSize=10, fontName="Helvetica-Bold", textColor=ORANGE_COL, alignment=TA_CENTER)),
    ])
    marks_table = Table(marks_data, colWidths=col_w)
    n = len(marks_data)
    marks_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), DARK), ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        *[("BACKGROUND", (0,r), (-1,r), GRAY if r%2==0 else WHITE) for r in range(1, n-1)],
        ("BACKGROUND", (0,n-1), (-1,n-1), LIGHT), ("FONTNAME", (0,n-1), (-1,n-1), "Helvetica-Bold"),
        ("BOX", (0,0), (-1,-1), 1, MED), ("INNERGRID", (0,0), (-1,-1), 0.3, colors.HexColor("#C0D4E8")),
        ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 8), ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("ALIGN", (1,1), (1,n-1), "LEFT"),
    ]))
    story.append(marks_table)
    story.append(Spacer(1, 0.6*cm))

    summary_data = [[Paragraph("Overall Percentage", label_style), Paragraph(f"{overall_pct:.2f}%", grade_style),
                     Paragraph("Grade", label_style), Paragraph(overall_grade, grade_style),
                     Paragraph("Result", label_style), Paragraph(overall_remark, remark_style)]]
    summary_table = Table(summary_data, colWidths=[3.5*cm, 3*cm, 2*cm, 2*cm, 2.5*cm, 4.4*cm])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), LIGHT), ("BOX", (0,0), (-1,-1), 1.5, DARK),
        ("INNERGRID", (0,0), (-1,-1), 0.5, MED), ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10), ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8), ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.8*cm))

    legend = [["Grade Scale:", "A+(≥90)", "A(≥80)", "B+(≥70)", "B(≥60)", "C(≥50)", "D(≥40)", "F(<40)"]]
    legend_table = Table(legend, colWidths=[2.5*cm]+[2.1*cm]*7)
    legend_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), DARK), ("BACKGROUND", (1,0), (-1,0), GRAY),
        ("TEXTCOLOR", (0,0), (0,0), WHITE), ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 8), ("BOX", (0,0), (-1,-1), 0.5, MED),
        ("INNERGRID", (0,0), (-1,-1), 0.3, MED), ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(legend_table)
    story.append(Spacer(1, 1.2*cm))

    story.append(HRFlowable(width="100%", thickness=1, color=MED, spaceBefore=0, spaceAfter=4))
    story.append(Paragraph(f"Generated by Student Result Management System (SRMS)  |  A.S. College, Khanna  |  {datetime.now().strftime('%d %b %Y, %I:%M %p')}", footer_style))
    doc.build(story)


class resultClass:
    def __init__(self, root):
        self.root = root
        self.root.title("SRMS — Enter Student Results")
        self.root.geometry("1350x750+50+50")
        self.root.config(bg=BG)
        self.root.focus_force()

        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.var_subject = StringVar()
        self.var_obtained = StringVar()
        self.var_full = StringVar()

        self.roll_list = []
        self.subjects = []
        self.entry_fields = []

        self._build_layout()
        self._fetch_rolls()

    def _build_layout(self):
        # Title Bar
        title_bar = Frame(self.root, bg=ACCENT2, height=55)
        title_bar.pack(fill=X, side=TOP)
        title_bar.pack_propagate(False)
        Label(title_bar, text="📝  Enter Student Results",
              font=("Segoe UI", 18, "bold"), bg=ACCENT2, fg="white").pack(side=LEFT, padx=20, pady=10)

        body = Frame(self.root, bg=BG)
        body.pack(fill=BOTH, expand=True, padx=20, pady=15)

        # Left Panel (Student + Subject entry)
        left_container = LabelFrame(body, text=" Student & Subject Details ",
                                    font=("Segoe UI", 12, "bold"),
                                    bg=CARD_BG, fg=ACCENT2, bd=2, relief=GROOVE)
        left_container.pack(side=LEFT, fill=Y, padx=(0, 15), ipadx=10, ipady=10)

        # Scrollable frame
        canvas = Canvas(left_container, bg=CARD_BG, highlightthickness=0)
        scrollbar = Scrollbar(left_container, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=CARD_BG)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=400)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        form_frame = scrollable_frame
        form_frame.columnconfigure(0, weight=1)

        # Roll No
        Label(form_frame, text="Roll No.", font=FONT_TITLE, bg=CARD_BG, fg=TEXT_SECONDARY).grid(row=0, column=0, padx=15, pady=(15,5), sticky=W)
        self.cmb_roll = ttk.Combobox(form_frame, textvariable=self.var_roll, values=self.roll_list,
                                     font=FONT_BODY, state="readonly", width=35)
        self.cmb_roll.grid(row=1, column=0, padx=15, pady=(0,10), sticky=EW)
        self.cmb_roll.bind("<Return>", lambda e: self._search())

        btn_search = Button(form_frame, text="🔍 Search Student", font=FONT_TITLE,
                            bg=ACCENT, fg="white", cursor="hand2", relief=FLAT,
                            command=self._search, pady=5)
        btn_search.grid(row=2, column=0, padx=15, pady=5, sticky=EW)
        btn_search.bind("<Return>", lambda e: self._search())

        Label(form_frame, text="Name", font=FONT_TITLE, bg=CARD_BG, fg=TEXT_SECONDARY).grid(row=3, column=0, padx=15, pady=(15,5), sticky=W)
        self.txt_name = Entry(form_frame, textvariable=self.var_name, font=FONT_BODY,
                              bg=ENTRY_BG, fg=TEXT_PRIMARY, relief=SOLID, bd=1,
                              state="readonly", readonlybackground=ENTRY_BG)
        self.txt_name.grid(row=4, column=0, padx=15, pady=(0,10), sticky=EW)

        Label(form_frame, text="Course", font=FONT_TITLE, bg=CARD_BG, fg=TEXT_SECONDARY).grid(row=5, column=0, padx=15, pady=(5,5), sticky=W)
        self.txt_course = Entry(form_frame, textvariable=self.var_course, font=FONT_BODY,
                                bg=ENTRY_BG, fg=TEXT_PRIMARY, relief=SOLID, bd=1,
                                state="readonly", readonlybackground=ENTRY_BG)
        self.txt_course.grid(row=6, column=0, padx=15, pady=(0,15), sticky=EW)

        Frame(form_frame, bg=BORDER_COLOR, height=2).grid(row=7, column=0, padx=15, pady=10, sticky=EW)

        Label(form_frame, text="➕ Add Subject Marks", font=FONT_TITLE, bg=CARD_BG, fg=ACCENT2).grid(row=8, column=0, padx=15, pady=(10,10), sticky=W)

        Label(form_frame, text="Subject Name", font=FONT_TITLE, bg=CARD_BG, fg=TEXT_SECONDARY).grid(row=9, column=0, padx=15, pady=(5,5), sticky=W)
        self.txt_subject = Entry(form_frame, textvariable=self.var_subject, font=FONT_BODY,
                                 bg=ENTRY_BG, fg=TEXT_PRIMARY, relief=SOLID, bd=1)
        self.txt_subject.grid(row=10, column=0, padx=15, pady=(0,10), sticky=EW)
        self.txt_subject.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_subject)

        Label(form_frame, text="Marks Obtained", font=FONT_TITLE, bg=CARD_BG, fg=TEXT_SECONDARY).grid(row=11, column=0, padx=15, pady=(5,5), sticky=W)
        self.txt_obtained = Entry(form_frame, textvariable=self.var_obtained, font=FONT_BODY,
                                  bg=ENTRY_BG, fg=TEXT_PRIMARY, relief=SOLID, bd=1)
        self.txt_obtained.grid(row=12, column=0, padx=15, pady=(0,10), sticky=EW)
        self.txt_obtained.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_obtained)

        Label(form_frame, text="Full Marks", font=FONT_TITLE, bg=CARD_BG, fg=TEXT_SECONDARY).grid(row=13, column=0, padx=15, pady=(5,5), sticky=W)
        self.txt_full = Entry(form_frame, textvariable=self.var_full, font=FONT_BODY,
                              bg=ENTRY_BG, fg=TEXT_PRIMARY, relief=SOLID, bd=1)
        self.txt_full.grid(row=14, column=0, padx=15, pady=(0,10), sticky=EW)
        self.txt_full.bind("<Return>", self._on_enter_pressed)
        self.entry_fields.append(self.txt_full)

        btn_add = Button(form_frame, text="➕ Add Subject", font=FONT_TITLE, bg=GREEN, fg="white",
                         cursor="hand2", relief=FLAT, command=self._add_subject, pady=6)
        btn_add.grid(row=15, column=0, padx=15, pady=(10,5), sticky=EW)
        btn_add.bind("<Return>", lambda e: self._add_subject())

        btn_frame = Frame(form_frame, bg=CARD_BG)
        btn_frame.grid(row=16, column=0, padx=15, pady=(15,20), sticky=EW)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)

        btn_save = Button(btn_frame, text="💾 Save All", font=FONT_TITLE, bg=GREEN, fg="white",
                          cursor="hand2", relief=FLAT, command=self._save_all, pady=8)
        btn_save.grid(row=0, column=0, padx=5, sticky=EW)
        btn_save.bind("<Return>", lambda e: self._save_all())

        btn_remove = Button(btn_frame, text="🗑 Remove Row", font=FONT_TITLE, bg=RED, fg="white",
                            cursor="hand2", relief=FLAT, command=self._remove_row, pady=8)
        btn_remove.grid(row=0, column=1, padx=5, sticky=EW)
        btn_remove.bind("<Return>", lambda e: self._remove_row())

        btn_clear = Button(btn_frame, text="✖ Clear", font=FONT_TITLE, bg="#7F8C8D", fg="white",
                           cursor="hand2", relief=FLAT, command=self._clear, pady=8)
        btn_clear.grid(row=0, column=2, padx=5, sticky=EW)
        btn_clear.bind("<Return>", lambda e: self._clear())

        # Right Panel - Subjects Table
        right_panel = Frame(body, bg=BG)
        right_panel.pack(side=LEFT, fill=BOTH, expand=True)

        table_frame = LabelFrame(right_panel, text=" Subjects & Marks ",
                                 font=("Segoe UI", 12, "bold"), bg=CARD_BG, fg=ACCENT2, bd=2, relief=GROOVE)
        table_frame.pack(fill=BOTH, expand=True, pady=(0,10))

        cols = ("S.No", "Subject", "Marks Obtained", "Full Marks", "Percentage", "Grade")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                        background=ACCENT2, foreground="white")
        style.configure("Treeview", font=FONT_BODY, rowheight=28,
                        background=CARD_BG, foreground=TEXT_PRIMARY, fieldbackground=CARD_BG)
        style.map('Treeview', background=[('selected', ACCENT)])

        widths = [50, 300, 130, 110, 110, 80]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor=CENTER)
        self.tree.column("Subject", anchor=W)

        scroll = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y)
        self.tree.pack(fill=BOTH, expand=True, padx=5, pady=5)

        self.tree.tag_configure("odd", background="#F8FAFC")
        self.tree.tag_configure("even", background="#FFFFFF")
        self.tree.tag_configure("fail", background="#FEE2E2")

        self.lbl_summary = Label(right_panel, text="Total: 0 / 0   |   Percentage: 0.00%   |   Grade: —   |   Result: —",
                                 font=FONT_TITLE, bg=ACCENT2, fg="white", relief=FLAT, anchor=CENTER, pady=8)
        self.lbl_summary.pack(fill=X, pady=(0,8))

        btn_pdf = Button(right_panel, text="📄 Generate PDF Result Card", font=FONT_TITLE, bg=ORANGE, fg="white",
                         cursor="hand2", relief=FLAT, command=self._generate_pdf, pady=10)
        btn_pdf.pack(fill=X)
        btn_pdf.bind("<Return>", lambda e: self._generate_pdf())

    def _on_enter_pressed(self, event):
        current = event.widget
        try:
            idx = self.entry_fields.index(current)
            if idx < len(self.entry_fields) - 1:
                self.entry_fields[idx + 1].focus()
            else:
                self._add_subject()
        except ValueError:
            pass
        return "break"

    def _fetch_rolls(self):
        try:
            con = sqlite3.connect("rms.db")
            cur = con.cursor()
            cur.execute("SELECT roll FROM student")
            self.roll_list = [str(r[0]) for r in cur.fetchall()]
            con.close()
            self.cmb_roll['values'] = self.roll_list
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _search(self):
        if not self.var_roll.get():
            messagebox.showwarning("Input", "Please select a roll number.", parent=self.root)
            return
        try:
            con = sqlite3.connect("rms.db")
            cur = con.cursor()
            cur.execute("SELECT name, course FROM student WHERE roll=?", (self.var_roll.get(),))
            row = cur.fetchone()
            if row:
                self.var_name.set(row[0])
                self.var_course.set(row[1])
                cur.execute("SELECT course, marks_obtained, full_marks FROM result WHERE roll=? AND name=?",
                            (self.var_roll.get(), row[0]))
                results = cur.fetchall()
                self.subjects.clear()
                for subj, obt, full in results:
                    self.subjects.append({"subject": subj, "obtained": float(obt), "full": float(full)})
                self._refresh_tree()
                con.close()
                if self.subjects:
                    messagebox.showinfo("Loaded", f"Loaded {len(self.subjects)} existing subject(s).", parent=self.root)
                self.txt_subject.focus()
            else:
                messagebox.showerror("Not Found", "No student with that roll number.", parent=self.root)
                con.close()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _add_subject(self):
        subj = self.var_subject.get().strip()
        obt = self.var_obtained.get().strip()
        full = self.var_full.get().strip()
        if not subj:
            messagebox.showwarning("Input", "Subject name is required.", parent=self.root)
            self.txt_subject.focus()
            return
        if not self.var_name.get():
            messagebox.showwarning("Input", "Please search a student first.", parent=self.root)
            return
        try:
            obt_f = float(obt)
            full_f = float(full)
        except ValueError:
            messagebox.showerror("Error", "Marks must be numeric.", parent=self.root)
            self.txt_obtained.focus()
            return
        if obt_f > full_f:
            messagebox.showerror("Error", "Marks obtained cannot exceed full marks.", parent=self.root)
            self.txt_obtained.focus()
            return
        if full_f <= 0:
            messagebox.showerror("Error", "Full marks must be greater than 0.", parent=self.root)
            self.txt_full.focus()
            return
        if any(s["subject"].lower() == subj.lower() for s in self.subjects):
            messagebox.showwarning("Duplicate", f"'{subj}' is already added.", parent=self.root)
            return
        self.subjects.append({"subject": subj, "obtained": obt_f, "full": full_f})
        self._refresh_tree()
        self.var_subject.set("")
        self.var_obtained.set("")
        self.var_full.set("")
        self.txt_subject.focus()

    def _refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        total_obt = 0
        total_full = 0
        for i, s in enumerate(self.subjects):
            pct = (s["obtained"] / s["full"] * 100) if s["full"] > 0 else 0
            grade = grade_from_pct(pct)
            tag = "fail" if pct < 40 else ("even" if i % 2 == 0 else "odd")
            self.tree.insert("", END, values=(i+1, s["subject"],
                             int(s["obtained"]) if s["obtained"].is_integer() else s["obtained"],
                             int(s["full"]) if s["full"].is_integer() else s["full"],
                             f"{pct:.1f}%", grade), tags=(tag,))
            total_obt += s["obtained"]
            total_full += s["full"]
        if total_full > 0:
            overall = total_obt / total_full * 100
            grade = grade_from_pct(overall)
            remark = remark_from_pct(overall)
            self.lbl_summary.config(
                text=f"Total: {int(total_obt)} / {int(total_full)}   |   Percentage: {overall:.2f}%   |   Grade: {grade}   |   Result: {remark}",
                bg=GREEN if overall >= 40 else RED
            )
        else:
            self.lbl_summary.config(text="Total: 0 / 0   |   Percentage: 0.00%   |   Grade: —   |   Result: —", bg=ACCENT2)

    def _remove_row(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select", "Click a subject row to remove.", parent=self.root)
            return
        idx = int(self.tree.item(selected[0])["values"][0]) - 1
        subject_to_remove = self.subjects[idx]["subject"]
        if messagebox.askyesno("Confirm", f"Permanently delete '{subject_to_remove}' for {self.var_name.get()}?", parent=self.root):
            self.subjects.pop(idx)
            # Also delete from database if it exists
            try:
                con = sqlite3.connect("rms.db")
                cur = con.cursor()
                cur.execute("DELETE FROM result WHERE roll=? AND name=? AND course=?",
                            (self.var_roll.get(), self.var_name.get(), subject_to_remove))
                con.commit()
                con.close()
            except Exception as ex:
                messagebox.showerror("Error", f"Could not delete from database: {str(ex)}", parent=self.root)
            self._refresh_tree()
            messagebox.showinfo("Deleted", f"'{subject_to_remove}' has been permanently removed.", parent=self.root)

    def _clear(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_course.set("")
        self.var_subject.set("")
        self.var_obtained.set("")
        self.var_full.set("")
        self.subjects.clear()
        self._refresh_tree()
        self.cmb_roll.focus()

    def _save_all(self):
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
                cur.execute("SELECT * FROM result WHERE roll=? AND name=? AND course=?",
                            (self.var_roll.get(), self.var_name.get(), s["subject"]))
                if cur.fetchone():
                    skipped += 1
                    continue
                pct = (s["obtained"] / s["full"] * 100) if s["full"] > 0 else 0
                cur.execute("INSERT INTO result(roll, name, course, marks_obtained, full_marks, percentage) VALUES(?,?,?,?,?,?)",
                            (self.var_roll.get(), self.var_name.get(), s["subject"],
                             str(s["obtained"]), str(s["full"]), f"{pct:.2f}"))
                saved += 1
            con.commit()
            con.close()
            msg = f"{saved} result(s) saved successfully."
            if skipped:
                msg += f"\n{skipped} subject(s) already existed and were skipped."
            messagebox.showinfo("Saved", msg, parent=self.root)
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
            messagebox.showerror("Missing Library", "reportlab is not installed.\nRun: pip install reportlab", parent=self.root)
            return
        student_info = {"roll": self.var_roll.get(), "name": self.var_name.get(), "course": self.var_course.get()}
        filename = f"Result_{self.var_roll.get()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        save_path = os.path.join(os.getcwd(), filename)
        try:
            generate_result_pdf(student_info, self.subjects, save_path)
            messagebox.showinfo("PDF Generated", f"Result card saved as:\n{filename}\n\nOpening PDF...", parent=self.root)
            os.startfile(save_path) if os.name == "nt" else os.system(f"xdg-open '{save_path}'")
        except Exception as ex:
            messagebox.showerror("PDF Error", str(ex), parent=self.root)


if __name__ == "__main__":
    root= Tk()
    root.tk.call('tk', 'scaling', 1.4)
    obj = resultClass(root)
    root.mainloop()