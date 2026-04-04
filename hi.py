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

class RMS:
    def __init__(self, root):
        self.root = root
        self.root.title("STUDENT RESULT MANAGEMENT SYSTEM")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#F0F4F8")
        
        # Load logo
        try:
            img = Image.open("images/logo_p.png")
            img = img.resize((45, 45), Image.Resampling.LANCZOS)
            self.logo_dash = ImageTk.PhotoImage(img)
        except:
            self.logo_dash = None
        
        # Title Bar
        self._create_title_bar()
        
        # Menu Bar
        self._create_menu_bar()
        
        # Main Content Area
        self._create_content_area()
        
        # Footer
        self._create_footer()
        
        # Update dashboard stats
        self.update_details()
        
        # Start clock
        self.update_clock()
    
    def _create_title_bar(self):
        """Create modern title bar"""
        title_frame = Frame(self.root, bg="#1A3E6F", height=60)
        title_frame.pack(fill=X, side=TOP)
        title_frame.pack_propagate(False)
        
        # Logo and title
        if self.logo_dash:
            lbl_logo = Label(title_frame, image=self.logo_dash, bg="#1A3E6F")
            lbl_logo.place(x=20, y=8)
        
        lbl_title = Label(title_frame, text="STUDENT RESULT MANAGEMENT SYSTEM",
                         font=("Segoe UI", 18, "bold"), bg="#1A3E6F", fg="white")
        lbl_title.place(x=75, y=15)
        
        # Date and Time in title bar
        self.lbl_datetime = Label(title_frame, font=("Segoe UI", 10),
                                  bg="#1A3E6F", fg="#A8C4E0")
        self.lbl_datetime.place(x=1050, y=20)
        self._update_datetime()
    
    def _create_menu_bar(self):
        """Create modern menu bar with buttons"""
        menu_frame = Frame(self.root, bg="white", height=70)
        menu_frame.pack(fill=X, side=TOP, padx=20, pady=(15, 0))
        menu_frame.pack_propagate(False)
        
        # Menu buttons
        menus = [
            ("📚 Courses", self.add_course, "#2B6CB0"),
            ("👨‍🎓 Students", self.add_student, "#2B6CB0"),
            ("📝 Results", self.add_result, "#2B6CB0"),
            ("📊 View Results", self.add_report, "#2B6CB0"),
            ("🚪 Logout", self.logout, "#C0392B"),
            ("✖ Exit", self.exit_, "#7F8C8D")
        ]
        
        x_pos = 20
        for text, cmd, color in menus:
            btn = Button(menu_frame, text=text, font=("Segoe UI", 11, "bold"),
                        bg=color, fg="white", cursor="hand2", relief=FLAT,
                        activebackground="#1A3E6F", activeforeground="white",
                        command=cmd, padx=20, pady=8)
            btn.place(x=x_pos, y=12)
            x_pos += 170
        
        # Welcome message
        lbl_welcome = Label(menu_frame, text="Welcome back!", font=("Segoe UI", 11),
                           bg="white", fg="#2B6CB0")
        lbl_welcome.place(x=1150, y=22)
    
    def _create_content_area(self):
        """Create main content area with stats cards"""
        # Stats Cards
        self.lbl_course = self._create_stat_card(
            "📚", "Total Courses", "#E8692A", 50, 180
        )
        self.lbl_student = self._create_stat_card(
            "👨‍🎓", "Total Students", "#2B6CB0", 470, 180
        )
        self.lbl_result = self._create_stat_card(
            "📝", "Total Results", "#1ABC9C", 890, 180
        )
        
        # Clock Display
        clock_frame = Frame(self.root, bg="white", bd=2, relief=GROOVE)
        clock_frame.place(x=50, y=330, width=300, height=300)
        
        self.clock_lbl = Label(clock_frame, bg="white")
        self.clock_lbl.pack(pady=20)
        
        self.lbl_time = Label(clock_frame, font=("Segoe UI", 24, "bold"),
                              bg="white", fg="#1A3E6F")
        self.lbl_time.pack()
        
        self.lbl_date = Label(clock_frame, font=("Segoe UI", 12),
                              bg="white", fg="#7F8C8D")
        self.lbl_date.pack(pady=5)
        
        # Info Panel
        info_frame = Frame(self.root, bg="white", bd=2, relief=GROOVE)
        info_frame.place(x=380, y=330, width=920, height=300)
        
        lbl_info_title = Label(info_frame, text="📌 Quick Actions",
                              font=("Segoe UI", 14, "bold"),
                              bg="white", fg="#1A3E6F")
        lbl_info_title.place(x=20, y=15)
        
        # Quick action buttons
        actions = [
            ("➕ Add New Course", self.add_course, "#E8692A", 30, 70),
            ("👨‍🎓 Register Student", self.add_student, "#2B6CB0", 30, 130),
            ("📝 Enter Results", self.add_result, "#1ABC9C", 30, 190),
            ("📊 View Reports", self.add_report, "#8E44AD", 30, 250),
        ]
        
        for text, cmd, color, x, y in actions:
            btn = Button(info_frame, text=text, font=("Segoe UI", 11),
                        bg=color, fg="white", cursor="hand2", relief=FLAT,
                        activebackground="#1A3E6F", command=cmd,
                        width=25, height=2)
            btn.place(x=x, y=y)
        
        # Recent activity
        lbl_recent = Label(info_frame, text="📋 Recent Activity",
                          font=("Segoe UI", 12, "bold"),
                          bg="white", fg="#1A3E6F")
        lbl_recent.place(x=350, y=15)
        
        self.activity_list = Listbox(info_frame, font=("Segoe UI", 10),
                                     bg="#F0F4F8", fg="#333", bd=0,
                                     highlightthickness=0, height=12)
        self.activity_list.place(x=350, y=50, width=540, height=220)
        
        # Sample activities
        sample_activities = [
            "🎉 Welcome to SRMS",
            "📚 System ready to use",
            "👨‍🎓 Add students to get started",
        ]
        for act in sample_activities:
            self.activity_list.insert(END, act)
    
    def _create_stat_card(self, icon, label, color, x, y):
        """Create a statistics card"""
        frame = Frame(self.root, bg=color, bd=0, relief=FLAT)
        frame.place(x=x, y=y, width=380, height=120)
        
        inner = Frame(frame, bg=color)
        inner.pack(fill=BOTH, expand=True, padx=15, pady=15)
        
        lbl_icon = Label(inner, text=icon, font=("Segoe UI", 32),
                         bg=color, fg="white")
        lbl_icon.pack(side=LEFT)
        
        right_frame = Frame(inner, bg=color)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        
        lbl_value = Label(right_frame, text="0", font=("Segoe UI", 28, "bold"),
                          bg=color, fg="white", anchor="e")
        lbl_value.pack(fill=X)
        
        lbl_label = Label(right_frame, text=label, font=("Segoe UI", 12),
                          bg=color, fg="white", anchor="e")
        lbl_label.pack(fill=X)
        
        return lbl_value
    
    def _create_footer(self):
        """Create footer"""
        footer = Frame(self.root, bg="#1A3E6F", height=35)
        footer.pack(side=BOTTOM, fill=X)
        
        lbl_footer = Label(footer, text="SRMS — Student Result Management System | A.S. College, Khanna",
                          font=("Segoe UI", 9), bg="#1A3E6F", fg="#A8C4E0")
        lbl_footer.pack(pady=8)
    
    def _update_datetime(self):
        """Update date and time display"""
        now = datetime.now()
        self.lbl_datetime.config(text=now.strftime("%d/%m/%Y  %I:%M %p"))
        self.root.after(60000, self._update_datetime)
    
    def update_clock(self):
        """Update analog clock"""
        now = datetime.now()
        h = now.hour % 12
        m = now.minute
        s = now.second
        
        hr_angle = (h / 12) * 360 + (m / 60) * 30
        min_angle = (m / 60) * 360
        sec_angle = (s / 60) * 360
        
        self._draw_clock(hr_angle, min_angle, sec_angle)
        
        self.lbl_time.config(text=now.strftime("%I:%M:%S %p"))
        self.lbl_date.config(text=now.strftime("%A, %d %B %Y"))
        
        self.root.after(1000, self.update_clock)
    
    def _draw_clock(self, hr, min_, sec):
        """Draw analog clock"""
        size = 200
        cx = cy = size // 2
        img = Image.new("RGB", (size, size), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Clock face
        draw.ellipse((5, 5, size-5, size-5), outline="#1A3E6F", width=3)
        draw.ellipse((12, 12, size-12, size-12), outline="#D9E8F5", width=1)
        
        # Hour markers
        for i in range(12):
            angle = radians(i * 30)
            r1, r2 = cx - 15, cx - 8
            draw.line((cx + r1 * sin(angle), cy - r1 * cos(angle),
                       cx + r2 * sin(angle), cy - r2 * cos(angle)),
                      fill="#2B6CB0", width=3 if i % 3 == 0 else 1)
        
        # Hands
        def draw_hand(angle, length, color, width):
            rad = radians(angle)
            draw.line((cx, cy, cx + length * sin(rad), cy - length * cos(rad)),
                      fill=color, width=width)
        
        draw_hand(hr, 60, "#E8692A", 5)
        draw_hand(min_, 85, "#1ABC9C", 3)
        draw_hand(sec, 90, "#2B6CB0", 2)
        
        # Center dot
        draw.ellipse((cx-5, cy-5, cx+5, cy+5), fill="#E8692A")
        
        self.clock_img = ImageTk.PhotoImage(img)
        self.clock_lbl.config(image=self.clock_img)
    
    def update_details(self):
        """Update dashboard statistics"""
        try:
            con = sqlite3.connect("rms.db")
            cur = con.cursor()
            
            cur.execute("SELECT COUNT(*) FROM course")
            self.lbl_course.config(text=str(cur.fetchone()[0]))
            
            cur.execute("SELECT COUNT(*) FROM student")
            self.lbl_student.config(text=str(cur.fetchone()[0]))
            
            cur.execute("SELECT COUNT(*) FROM result")
            self.lbl_result.config(text=str(cur.fetchone()[0]))
            
            con.close()
        except:
            self.lbl_course.config(text="0")
            self.lbl_student.config(text="0")
            self.lbl_result.config(text="0")
        
        self.root.after(5000, self.update_details)
    
    def add_activity(self, activity):
        """Add activity to list"""
        self.activity_list.insert(0, f"• {activity}")
        if self.activity_list.size() > 20:
            self.activity_list.delete(END)
    
    def add_course(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CourseClass(self.new_win)
        self.add_activity("Opened Course Management")
    
    def add_student(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = studentClass(self.new_win)
        self.add_activity("Opened Student Management")
    
    def add_result(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = resultClass(self.new_win)
        self.add_activity("Opened Result Entry")
    
    def add_report(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = reportClass(self.new_win)
        self.add_activity("Opened Report Viewer")
    
    def logout(self):
        op = messagebox.askyesno("Confirm", "Do you really want to logout?", parent=self.root)
        if op:
            self.root.destroy()
            os.system("python login.py")
    
    def exit_(self):
        op = messagebox.askyesno("Confirm", "Do you really want to exit?", parent=self.root)
        if op:
            self.root.destroy()


if __name__ == "__main__":
    root= Tk()
    root.tk.call('tk', 'scaling', 1.4)
    obj = RMS(root)
    root.mainloop()