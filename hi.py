
from tkinter import *
from datetime import datetime
from math import sin, cos, radians
from PIL import Image, ImageTk, ImageDraw
from course import CourseClass
from student import studentClass
from result import resultClass
from report import reportClass
from tkinter import messagebox
import sqlite3
import os

# ── Colour palette ────────────────────────────────────────────────────────────
BG        = "#0F1C2E"   # page background (near-black navy)
SIDEBAR   = "#0A1628"   # sidebar
CARD_BG   = "#162032"   # stat cards
TOPBAR    = "#111E30"   # top bar
ACCENT    = "#2B6CB0"   # primary blue
ACCENT2   = "#1A3E6F"   # darker blue
GREEN     = "#1ABC9C"
ORANGE    = "#E8692A"
PURPLE    = "#7C3AED"
TEXT      = "#E8EDF4"
SUBTEXT   = "#8CA0B8"
WHITE     = "#FFFFFF"
SEP       = "#1E2E42"   # separator lines

FONT_TITLE  = ("Segoe UI", 11, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)
FONT_LARGE  = ("Segoe UI", 22, "bold")
FONT_MEDIUM = ("Segoe UI", 14, "bold")


class RMS:
    def __init__(self, root):
        self.root = root
        self.root.title("SRMS — Student Result Management System")
        self.root.geometry("1380x760+0+0")
        self.root.config(bg=BG)
        self.root.resizable(True, True)

        self._build_layout()
        self.update_details()
        self._update_clock()
        self._update_datetime()

    # ── Layout skeleton ───────────────────────────────────────────────────────
    def _build_layout(self):
        # ── Sidebar ──────────────────────────────────────────────────────────
        self.sidebar = Frame(self.root, bg=SIDEBAR, width=220)
        self.sidebar.pack(side=LEFT, fill=Y)
        self.sidebar.pack_propagate(False)

        # Logo area
        logo_frame = Frame(self.sidebar, bg=ACCENT2, height=80)
        logo_frame.pack(fill=X)
        logo_frame.pack_propagate(False)
        Label(logo_frame, text="🎓", font=("Segoe UI", 26), bg=ACCENT2, fg=WHITE
              ).place(relx=0.18, rely=0.5, anchor=CENTER)
        Label(logo_frame, text="SRMS", font=("Segoe UI", 16, "bold"), bg=ACCENT2, fg=WHITE
              ).place(relx=0.62, rely=0.35, anchor=CENTER)
        Label(logo_frame, text="Result Management", font=("Segoe UI", 8), bg=ACCENT2, fg="#A8C4E0"
              ).place(relx=0.62, rely=0.68, anchor=CENTER)

        # Nav label
        Label(self.sidebar, text="  NAVIGATION", font=("Segoe UI", 8, "bold"),
              bg=SIDEBAR, fg=SUBTEXT, anchor=W).pack(fill=X, padx=10, pady=(18, 4))

        Frame(self.sidebar, bg=SEP, height=1).pack(fill=X, padx=12)

        # Nav buttons
        self._nav_btn("📚  Manage Courses",    self.add_course)
        self._nav_btn("👨‍🎓  Manage Students",  self.add_student)
        self._nav_btn("📝  Enter Results",     self.add_result)
        self._nav_btn("📊  View Results",      self.add_report)

        Frame(self.sidebar, bg=SEP, height=1).pack(fill=X, padx=12, pady=(14, 0))
        Label(self.sidebar, text="  ACCOUNT", font=("Segoe UI", 8, "bold"),
              bg=SIDEBAR, fg=SUBTEXT, anchor=W).pack(fill=X, padx=10, pady=(10, 4))

        self._nav_btn("🚪  Log Out", self.logout,  hover_color="#922B21", color="#C0392B")
        self._nav_btn("✖   Exit",   self.exit_,    hover_color="#555", color="#666")

        # Sidebar footer
        Frame(self.sidebar, bg=SEP, height=1).pack(fill=X, padx=12, side=BOTTOM, pady=(0, 8))
        Label(self.sidebar, text="A.S. College, Khanna\nBCA 3rd Year — 2024-25",
              font=("Segoe UI", 8), bg=SIDEBAR, fg=SUBTEXT, justify=CENTER
              ).pack(side=BOTTOM, pady=(0, 8))

        # ── Main area ────────────────────────────────────────────────────────
        main = Frame(self.root, bg=BG)
        main.pack(side=LEFT, fill=BOTH, expand=True)

        # Top bar
        topbar = Frame(main, bg=TOPBAR, height=60)
        topbar.pack(fill=X)
        topbar.pack_propagate(False)

        Label(topbar, text="Dashboard", font=("Segoe UI", 16, "bold"),
              bg=TOPBAR, fg=WHITE).pack(side=LEFT, padx=22, pady=12)

        # Live date + time in topbar
        self.lbl_datetime = Label(topbar, text="", font=("Segoe UI", 10),
                                   bg=TOPBAR, fg=SUBTEXT)
        self.lbl_datetime.pack(side=RIGHT, padx=22)

        Frame(topbar, bg=ACCENT, width=3).pack(side=RIGHT, fill=Y, pady=12)

        # ── Content ──────────────────────────────────────────────────────────
        content = Frame(main, bg=BG)
        content.pack(fill=BOTH, expand=True, padx=18, pady=14)

        # Row 1: stat cards + clock side by side
        row1 = Frame(content, bg=BG)
        row1.pack(fill=X, pady=(0, 14))

        # Stat cards column (left)
        stats_col = Frame(row1, bg=BG)
        stats_col.pack(side=LEFT, fill=BOTH, expand=True)

        # Welcome banner
        welcome = Frame(stats_col, bg=ACCENT2, height=58)
        welcome.pack(fill=X, pady=(0, 14))
        welcome.pack_propagate(False)
        Label(welcome, text="👋  Welcome to the Student Result Management System",
              font=("Segoe UI", 13, "bold"), bg=ACCENT2, fg=WHITE
              ).pack(side=LEFT, padx=18, pady=12)
        Label(welcome, text="A.S. College, Khanna",
              font=("Segoe UI", 10), bg=ACCENT2, fg="#A8C4E0"
              ).pack(side=RIGHT, padx=18)

        # Stat cards
        cards_row = Frame(stats_col, bg=BG)
        cards_row.pack(fill=X)

        self.lbl_course_num  = StringVar(value="0")
        self.lbl_student_num = StringVar(value="0")
        self.lbl_result_num  = StringVar(value="0")

        self._stat_card(cards_row, "📚", "Total Courses",  self.lbl_course_num,  ORANGE, 0)
        self._stat_card(cards_row, "👨‍🎓", "Total Students", self.lbl_student_num, GREEN,  1)
        self._stat_card(cards_row, "📝", "Total Results",  self.lbl_result_num,  PURPLE, 2)

        for i in range(3):
            cards_row.columnconfigure(i, weight=1)

        # Quick action buttons row
        qa_frame = LabelFrame(stats_col, text="  Quick Actions",
                              font=("Segoe UI", 10, "bold"),
                              bg=CARD_BG, fg=SUBTEXT, bd=0, relief=FLAT,
                              labelanchor=NW)
        qa_frame.pack(fill=X, pady=(14, 0), ipady=10)

        actions = [
            ("📚  Add Course",    self.add_course,  ACCENT),
            ("👨‍🎓  Add Student",  self.add_student, GREEN),
            ("📝  Enter Result",  self.add_result,  ORANGE),
            ("📊  View Results",  self.add_report,  PURPLE),
        ]
        for i, (txt, cmd, col) in enumerate(actions):
            btn = Button(qa_frame, text=txt, font=("Segoe UI", 10, "bold"),
                         bg=col, fg=WHITE, relief=FLAT, cursor="hand2",
                         activebackground=ACCENT2, activeforeground=WHITE,
                         command=cmd, pady=8)
            btn.grid(row=0, column=i, padx=8, pady=8, sticky=EW)
            qa_frame.columnconfigure(i, weight=1)

        # ── Clock column (right) ──────────────────────────────────────────────
        clock_col = Frame(row1, bg=CARD_BG, width=310)
        clock_col.pack(side=RIGHT, fill=Y, padx=(16, 0))
        clock_col.pack_propagate(False)

        Label(clock_col, text="🕐  Live Clock", font=("Segoe UI", 11, "bold"),
              bg=CARD_BG, fg=TEXT).pack(pady=(12, 4))
        Frame(clock_col, bg=SEP, height=1).pack(fill=X, padx=12)

        self.clock_lbl = Label(clock_col, bg=CARD_BG)
        self.clock_lbl.pack(pady=8)

        self.lbl_time_text = Label(clock_col, text="", font=("Segoe UI", 15, "bold"),
                                    bg=CARD_BG, fg=GREEN)
        self.lbl_time_text.pack()
        self.lbl_date_text = Label(clock_col, text="", font=("Segoe UI", 9),
                                    bg=CARD_BG, fg=SUBTEXT)
        self.lbl_date_text.pack(pady=(2, 12))

        # ── Footer ───────────────────────────────────────────────────────────
        footer = Frame(main, bg="#0A1628", height=32)
        footer.pack(fill=X, side=BOTTOM)
        footer.pack_propagate(False)
        Label(footer,
              text="SRMS — Student Result Management System  |  A.S. College, Khanna  |  Contact: 987654321",
              font=("Segoe UI", 8), bg="#0A1628", fg=SUBTEXT
              ).pack(expand=True)

    # ── Nav button ────────────────────────────────────────────────────────────
    def _nav_btn(self, text, command, color=None, hover_color=None):
        c  = color       or "#1C2E42"
        hc = hover_color or ACCENT
        btn = Button(self.sidebar, text=f"  {text}", font=("Segoe UI", 10),
                     bg=SIDEBAR, fg=TEXT, activebackground=hc, activeforeground=WHITE,
                     relief=FLAT, anchor=W, cursor="hand2", pady=9,
                     command=command)
        btn.pack(fill=X, padx=8, pady=2)
        btn.bind("<Enter>", lambda e: btn.config(bg=hc if hover_color else ACCENT, fg=WHITE))
        btn.bind("<Leave>", lambda e: btn.config(bg=SIDEBAR, fg=TEXT))

    # ── Stat card ─────────────────────────────────────────────────────────────
    def _stat_card(self, parent, icon, label, numvar, color, col):
        card = Frame(parent, bg=CARD_BG, bd=0, relief=FLAT)
        card.grid(row=0, column=col, padx=6, pady=4, sticky=NSEW)

        # Left colour bar
        Frame(card, bg=color, width=5).pack(side=LEFT, fill=Y)

        inner = Frame(card, bg=CARD_BG)
        inner.pack(side=LEFT, fill=BOTH, expand=True, padx=14, pady=16)

        Label(inner, text=icon, font=("Segoe UI", 24), bg=CARD_BG, fg=color
              ).pack(anchor=W)
        self._num_lbl = Label(inner, textvariable=numvar,
                               font=("Segoe UI", 32, "bold"), bg=CARD_BG, fg=WHITE)
        self._num_lbl.pack(anchor=W)

        # Store reference by label text for update_details
        lbl_widget = Label(inner, text=label, font=("Segoe UI", 10),
                            bg=CARD_BG, fg=SUBTEXT)
        lbl_widget.pack(anchor=W)

        # Hover effect
        for w in (card, inner, self._num_lbl, lbl_widget):
            w.bind("<Enter>", lambda e, c=card: c.config(bg="#1E2E42"))
            w.bind("<Leave>", lambda e, c=card: c.config(bg=CARD_BG))

    # ── Clock ─────────────────────────────────────────────────────────────────
    def _draw_clock(self, hr, min_, sec):
        size = 220
        cx = cy = size // 2
        img = Image.new("RGB", (size, size), (22, 32, 50))
        draw = ImageDraw.Draw(img)

        # Outer ring
        draw.ellipse((4, 4, size-4, size-4), outline="#2B6CB0", width=3)
        draw.ellipse((10, 10, size-10, size-10), outline="#1A3E6F", width=1)

        # Hour markers
        for i in range(12):
            a = radians(i * 30)
            r1, r2 = cx - 12, cx - 6
            draw.line((cx + r1*sin(a), cy - r1*cos(a),
                       cx + r2*sin(a), cy - r2*cos(a)),
                      fill="#4A7FB5", width=3 if i % 3 == 0 else 1)

        # Hands
        def hand(angle, length, color, width):
            a = radians(angle)
            draw.line((cx, cy, cx + length*sin(a), cy - length*cos(a)),
                      fill=color, width=width)

        hand(hr,   cx*0.50, "#E8692A", 5)  # hour  — orange
        hand(min_, cx*0.72, "#1ABC9C", 3)  # minute — green
        hand(sec,  cx*0.82, "#5B9BD5", 2)  # second — blue

        # Center dot
        draw.ellipse((cx-5, cy-5, cx+5, cy+5), fill="#E8692A")

        self._clock_photo = ImageTk.PhotoImage(img)
        self.clock_lbl.config(image=self._clock_photo)

    def _update_clock(self):
        now  = datetime.now()
        hr   = (now.hour % 12 / 12) * 360 + (now.minute / 60) * 30
        min_ = (now.minute / 60) * 360
        sec  = (now.second / 60) * 360
        self._draw_clock(hr, min_, sec)
        self.lbl_time_text.config(text=now.strftime("%I:%M:%S %p"))
        self.lbl_date_text.config(text=now.strftime("%A, %d %B %Y"))
        self.root.after(1000, self._update_clock)

    def _update_datetime(self):
        now = datetime.now()
        self.lbl_datetime.config(
            text=now.strftime("  📅  %A, %d %B %Y     🕐  %I:%M %p  ")
        )
        self.root.after(60000, self._update_datetime)

    # ── DB stats ─────────────────────────────────────────────────────────────
    def update_details(self):
        try:
            con = sqlite3.connect("rms.db")
            cur = con.cursor()
            cur.execute("select count(*) from course");  self.lbl_course_num.set(cur.fetchone()[0])
            cur.execute("select count(*) from student"); self.lbl_student_num.set(cur.fetchone()[0])
            cur.execute("select count(*) from result");  self.lbl_result_num.set(cur.fetchone()[0])
            con.close()
        except Exception as ex:
            pass
        self.root.after(3000, self.update_details)

    # ── Navigation ────────────────────────────────────────────────────────────
    def add_course(self):
        w = Toplevel(self.root); CourseClass(w)

    def add_student(self):
        w = Toplevel(self.root); studentClass(w)

    def add_result(self):
        w = Toplevel(self.root); resultClass(w)

    def add_report(self):
        w = Toplevel(self.root); reportClass(w)

    def logout(self):
        if messagebox.askyesno("Log Out", "Do you really want to log out?", parent=self.root):
            self.root.destroy()
            os.system("python login.py")

    def exit_(self):
        if messagebox.askyesno("Exit", "Do you really want to exit?", parent=self.root):
            self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = RMS(root)
    root.mainloop()