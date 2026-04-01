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

# ── Modern Color Palette ─────────────────────────────────────────────────────
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

# ── Modern Fonts ────────────────────────────────────────────────────────────
FONT_TITLE  = ("Segoe UI", 12, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)
FONT_LARGE  = ("Segoe UI", 24, "bold")
FONT_MEDIUM = ("Segoe UI", 15, "bold")


class RMS:
    def __init__(self, root):
        self.root = root
        self.root.title("SRMS — Student Result Management System")
        self.root.geometry("1400x800+0+0")
        self.root.config(bg=BG)
        self.root.resizable(True, True)

        self._build_layout()
        self.update_details()
        self._update_clock()
        self._update_datetime()

    # ── Modern Layout ─────────────────────────────────────────────────────────
    def _build_layout(self):
        # ── Enhanced Sidebar ──────────────────────────────────────────────────
        self.sidebar = Frame(self.root, bg=SIDEBAR, width=240)
        self.sidebar.pack(side=LEFT, fill=Y)
        self.sidebar.pack_propagate(False)

        # Logo area with shadow effect
        logo_frame = Frame(self.sidebar, bg=ACCENT2, height=90)
        logo_frame.pack(fill=X, pady=(0, 10))
        logo_frame.pack_propagate(False)
        
        # Modern logo design
        logo_canvas = Canvas(logo_frame, bg=ACCENT2, highlightthickness=0, height=90)
        logo_canvas.pack(fill=BOTH, expand=True)
        
        # Create gradient effect
        for i in range(90):
            color = f"#{int(42+(i*0.5)):02x}{int(97-(i*0.2)):02x}{int(238-(i*1.2)):02x}"
            logo_canvas.create_line(0, i, 240, i, fill=color, width=1)
        
        Label(logo_frame, text="🎓 SRMS", font=("Segoe UI", 18, "bold"), 
              bg=ACCENT2, fg=WHITE).place(relx=0.5, rely=0.4, anchor=CENTER)
        Label(logo_frame, text="Result Management", font=("Segoe UI", 9), 
              bg=ACCENT2, fg="#A8C4E0").place(relx=0.5, rely=0.7, anchor=CENTER)

        # Navigation header
        nav_header = Frame(self.sidebar, bg=SIDEBAR)
        nav_header.pack(fill=X, padx=15, pady=(20, 5))
        Label(nav_header, text="NAVIGATION", font=("Segoe UI", 10, "bold"),
              bg=SIDEBAR, fg=SUBTEXT).pack(side=LEFT)

        # Navigation buttons with modern styling
        self._nav_btn("📚  Manage Courses",    self.add_course)
        self._nav_btn("👨‍🎓  Manage Students",  self.add_student)
        self._nav_btn("📝  Enter Results",     self.add_result)
        self._nav_btn("📊  View Results",      self.add_report)

        # Account section
        acc_header = Frame(self.sidebar, bg=SIDEBAR)
        acc_header.pack(fill=X, padx=15, pady=(25, 5))
        Label(acc_header, text="ACCOUNT", font=("Segoe UI", 10, "bold"),
              bg=SIDEBAR, fg=SUBTEXT).pack(side=LEFT)

        self._nav_btn("🚪  Log Out", self.logout, hover_color="#E53E3E", color="#C53030")
        self._nav_btn("✖   Exit",   self.exit_,  hover_color="#718096", color="#4A5568")

        # Sidebar footer
        footer_frame = Frame(self.sidebar, bg=SIDEBAR)
        footer_frame.pack(side=BOTTOM, fill=X, pady=20)
        Label(footer_frame, text="A.S. College, Khanna\nBCA 3rd Year — 2024-25",
              font=("Segoe UI", 9), bg=SIDEBAR, fg=SUBTEXT, justify=CENTER
              ).pack()

        # ── Main Content Area ─────────────────────────────────────────────────
        main = Frame(self.root, bg=BG)
        main.pack(side=LEFT, fill=BOTH, expand=True)

        # Enhanced Top Bar
        topbar = Frame(main, bg=TOPBAR, height=70)
        topbar.pack(fill=X, padx=20, pady=20)
        topbar.pack_propagate(False)

        # Dashboard title with icon
        title_frame = Frame(topbar, bg=TOPBAR)
        title_frame.pack(side=LEFT)
        Label(title_frame, text="📊 Dashboard", font=("Segoe UI", 18, "bold"),
              bg=TOPBAR, fg=WHITE).pack(side=LEFT)

        # Date/time display with modern styling
        datetime_frame = Frame(topbar, bg=TOPBAR)
        datetime_frame.pack(side=RIGHT)
        
        self.lbl_datetime = Label(datetime_frame, text="", font=("Segoe UI", 11),
                                  bg=TOPBAR, fg=SUBTEXT)
        self.lbl_datetime.pack(side=LEFT, padx=10)

        # ── Content Area ──────────────────────────────────────────────────────
        content = Frame(main, bg=BG)
        content.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))

        # Welcome banner with gradient
        welcome = Frame(content, bg=ACCENT, height=70)
        welcome.pack(fill=X, pady=(0, 20))
        welcome.pack_propagate(False)
        
        # Create gradient background
        welcome_canvas = Canvas(welcome, bg=ACCENT, highlightthickness=0)
        welcome_canvas.pack(fill=BOTH, expand=True)
        
        # Bind configure to update gradient when resized
        def update_gradient(event):
            welcome_canvas.delete("gradient")
            for i in range(70):
                r = int(67 - (i * 0.2))
                g = int(97 - (i * 0.1))
                b = int(238 - (i * 0.5))
                color = f"#{r:02x}{g:02x}{b:02x}"
                welcome_canvas.create_line(0, i, event.width, i, fill=color, width=1, tags="gradient")
        
        welcome_canvas.bind("<Configure>", update_gradient)
        
        Label(welcome, text="👋 Welcome to the Student Result Management System",
              font=("Segoe UI", 14, "bold"), bg=ACCENT, fg=WHITE).place(relx=0.5, rely=0.5, anchor=CENTER)

        # Stat cards row
        cards_row = Frame(content, bg=BG)
        cards_row.pack(fill=X, pady=10)

        self.lbl_course_num  = StringVar(value="0")
        self.lbl_student_num = StringVar(value="0")
        self.lbl_result_num  = StringVar(value="0")

        self._stat_card(cards_row, "📚", "Total Courses",  self.lbl_course_num,  ORANGE, 0)
        self._stat_card(cards_row, "👨‍🎓", "Total Students", self.lbl_student_num, GREEN,  1)
        self._stat_card(cards_row, "📝", "Total Results",  self.lbl_result_num,  PURPLE, 2)

        for i in range(3):
            cards_row.columnconfigure(i, weight=1)

        # Quick actions row
        qa_frame = LabelFrame(content, text=" Quick Actions ", font=("Segoe UI", 11, "bold"),
                              bg=CARD_BG, fg=TEXT, bd=0, relief=FLAT, labelanchor=NW)
        qa_frame.pack(fill=X, pady=15, ipady=10)

        actions = [
            ("📚  Add Course",    self.add_course,  ACCENT),
            ("👨‍🎓  Add Student",  self.add_student, GREEN),
            ("📝  Enter Result",  self.add_result,  ORANGE),
            ("📊  View Results",  self.add_report,  PURPLE),
        ]
        
        for i, (txt, cmd, col) in enumerate(actions):
            btn = Button(qa_frame, text=txt, font=("Segoe UI", 11, "bold"),
                         bg=col, fg=WHITE, relief=FLAT, cursor="hand2",
                         activebackground=ACCENT2, activeforeground=WHITE,
                         command=cmd, pady=10)
            btn.grid(row=0, column=i, padx=8, pady=8, sticky=EW)
            qa_frame.columnconfigure(i, weight=1)

        # ── Clock and Statistics Row ───────────────────────────────────────────
        bottom_row = Frame(content, bg=BG)
        bottom_row.pack(fill=BOTH, expand=True, pady=15)

        # Left side - Recent Activity (placeholder)
        activity_frame = LabelFrame(bottom_row, text=" Recent Activity ", font=("Segoe UI", 11, "bold"),
                                     bg=CARD_BG, fg=TEXT, bd=0, relief=FLAT)
        activity_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 15))
        
        # Activity list
        activities = [
            "📝 New results added for Roll No: 4620",
            "👨‍🎓 Student Shashi Partap enrolled in Java",
            "📚 Course 'Python Programming' added",
            "📊 Report generated for 15 students"
        ]
        for act in activities:
            Label(activity_frame, text=act, font=FONT_BODY, bg=CARD_BG, fg=SUBTEXT, 
                  pady=8, anchor=W).pack(fill=X, padx=15)

        # Right side - Live Clock
        clock_frame = LabelFrame(bottom_row, text=" Live Clock ", font=("Segoe UI", 11, "bold"),
                                  bg=CARD_BG, fg=TEXT, bd=0, relief=FLAT)
        clock_frame.pack(side=RIGHT, fill=Y, padx=(15, 0))
        
        self.clock_lbl = Label(clock_frame, bg=CARD_BG)
        self.clock_lbl.pack(pady=15)
        
        self.lbl_time_text = Label(clock_frame, text="", font=("Segoe UI", 20, "bold"),
                                    bg=CARD_BG, fg=GREEN)
        self.lbl_time_text.pack()
        
        self.lbl_date_text = Label(clock_frame, text="", font=("Segoe UI", 11),
                                    bg=CARD_BG, fg=SUBTEXT)
        self.lbl_date_text.pack(pady=(5, 15))

        # Footer
        footer = Frame(main, bg=SIDEBAR, height=35)
        footer.pack(fill=X, side=BOTTOM)
        footer.pack_propagate(False)
        Label(footer, text="SRMS — Student Result Management System | A.S. College, Khanna | Contact: support@srms.edu",
              font=("Segoe UI", 9), bg=SIDEBAR, fg=SUBTEXT).pack(expand=True)

    # ── Nav button with hover effects ────────────────────────────────────────────
    def _nav_btn(self, text, command, color=None, hover_color=None):
        c  = color or "#1C2E42"
        hc = hover_color or ACCENT
        btn = Button(self.sidebar, text=f"  {text}", font=("Segoe UI", 10),
                     bg=SIDEBAR, fg=TEXT, activebackground=hc, activeforeground=WHITE,
                     relief=FLAT, anchor=W, cursor="hand2", pady=10,
                     command=command)
        btn.pack(fill=X, padx=8, pady=2)
        btn.bind("<Enter>", lambda e: btn.config(bg=hc if hover_color else ACCENT, fg=WHITE))
        btn.bind("<Leave>", lambda e: btn.config(bg=SIDEBAR, fg=TEXT))

    # ── Stat card with modern design ─────────────────────────────────────────────
    def _stat_card(self, parent, icon, label, numvar, color, col):
        card = Frame(parent, bg=CARD_BG, bd=0, relief=FLAT)
        card.grid(row=0, column=col, padx=8, pady=8, sticky=NSEW)

        # Left color bar
        Frame(card, bg=color, width=6).pack(side=LEFT, fill=Y)

        inner = Frame(card, bg=CARD_BG)
        inner.pack(side=LEFT, fill=BOTH, expand=True, padx=15, pady=15)

        Label(inner, text=icon, font=("Segoe UI", 28), bg=CARD_BG, fg=color
              ).pack(anchor=W)
        Label(inner, textvariable=numvar, font=("Segoe UI", 32, "bold"),
              bg=CARD_BG, fg=WHITE).pack(anchor=W)
        Label(inner, text=label, font=("Segoe UI", 10), bg=CARD_BG, fg=SUBTEXT
              ).pack(anchor=W)

        # Hover effect
        for w in (card, inner):
            w.bind("<Enter>", lambda e, c=card: c.config(bg=HOVER))
            w.bind("<Leave>", lambda e, c=card: c.config(bg=CARD_BG))

    # ── Clock drawing ─────────────────────────────────────────────────────────
    def _draw_clock(self, hr, min_, sec):
        size = 200
        cx = cy = size // 2
        img = Image.new("RGB", (size, size), (22, 32, 50))
        draw = ImageDraw.Draw(img)

        # Outer ring
        draw.ellipse((4, 4, size-4, size-4), outline=ACCENT, width=3)
        draw.ellipse((10, 10, size-10, size-10), outline=ACCENT2, width=1)

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

        hand(hr,   cx*0.50, ORANGE, 5)   # hour
        hand(min_, cx*0.70, GREEN, 3)    # minute
        hand(sec,  cx*0.80, ACCENT, 2)   # second

        # Center dot
        draw.ellipse((cx-4, cy-4, cx+4, cy+4), fill=ORANGE)

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
        self.lbl_datetime.config(text=now.strftime("📅 %d %b %Y | 🕐 %I:%M %p"))
        self.root.after(60000, self._update_datetime)

    # ── Database stats ─────────────────────────────────────────────────────────
    def update_details(self):
        try:
            con = sqlite3.connect("rms.db")
            cur = con.cursor()
            cur.execute("select count(*) from course")
            self.lbl_course_num.set(cur.fetchone()[0])
            cur.execute("select count(*) from student")
            self.lbl_student_num.set(cur.fetchone()[0])
            cur.execute("select count(*) from result")
            self.lbl_result_num.set(cur.fetchone()[0])
            con.close()
        except Exception as ex:
            pass
        self.root.after(3000, self.update_details)

    # ── Navigation methods ────────────────────────────────────────────────────
    def add_course(self):
        w = Toplevel(self.root)
        w.grab_set()
        CourseClass(w)

    def add_student(self):
        w = Toplevel(self.root)
        w.grab_set()
        studentClass(w)

    def add_result(self):
        w = Toplevel(self.root)
        w.grab_set()
        resultClass(w)

    def add_report(self):
        w = Toplevel(self.root)
        w.grab_set()
        reportClass(w)

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