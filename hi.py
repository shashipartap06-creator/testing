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
        
        # Main Content Area - Responsive
        self._create_content_area_responsive()
        
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
        
        # Date and Time in title bar - Positioned at right corner where white strip ends
        self.lbl_datetime = Label(title_frame, font=("Segoe UI", 11, "bold"),
                                  bg="#1A3E6F", fg="#7FD3FF", relief=RAISED, 
                                  padx=12, pady=5, bd=1)
        self.lbl_datetime.place(x=1330, y=18, anchor="ne")
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
        lbl_welcome = Label(menu_frame, text="Welcome back!", font=("Segoe UI", 11, "bold"),
                           bg="white", fg="#2B6CB0")
        lbl_welcome.place(x=1150, y=22)
    
    def _create_content_area_responsive(self):
        """Create main content area with decorative borders - RESPONSIVE"""
        
        # Padding frame
        padding_frame = Frame(self.root, bg="#F0F4F8")
        padding_frame.pack(fill=BOTH, expand=True, padx=20, pady=15)
        
        # Outer decorative frame (Orange border)
        outer_border = Frame(padding_frame, bg="#E8692A")
        outer_border.pack(fill=BOTH, expand=True)
        
        # Inner white frame with padding
        inner_frame = Frame(outer_border, bg="#F0F4F8")
        inner_frame.pack(fill=BOTH, expand=True, padx=8, pady=8)
        
        # Stats Cards Frame
        stats_frame = Frame(inner_frame, bg="#F0F4F8")
        stats_frame.pack(fill=X, padx=10, pady=10)
        
        # Create stat cards side by side
        self.lbl_course = self._create_stat_card_responsive(
            stats_frame, "📚", "Total Courses", "#E8692A", 0
        )
        self.lbl_student = self._create_stat_card_responsive(
            stats_frame, "👨‍🎓", "Total Students", "#2B6CB0", 1
        )
        self.lbl_result = self._create_stat_card_responsive(
            stats_frame, "📝", "Total Results", "#1ABC9C", 2
        )
        
        # Bottom content frame (Clock + Info)
        bottom_frame = Frame(inner_frame, bg="#F0F4F8")
        bottom_frame.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Left side - Clock
        clock_frame = Frame(bottom_frame, bg="white", bd=2, relief=GROOVE)
        clock_frame.pack(side=LEFT, fill=BOTH, expand=False, padx=(0, 10), pady=10)
        
        self.clock_lbl = Label(clock_frame, bg="white")
        self.clock_lbl.pack(pady=15)
        
        self.lbl_time = Label(clock_frame, font=("Segoe UI", 24, "bold"),
                              bg="white", fg="#1A3E6F")
        self.lbl_time.pack()
        
        self.lbl_date = Label(clock_frame, font=("Segoe UI", 12, "bold"),
                              bg="white", fg="#E8692A")
        self.lbl_date.pack(pady=5)
        
        # Right side - Info Panel with cyan border
        info_border = Frame(bottom_frame, bg="#00BCD4")
        info_border.pack(side=RIGHT, fill=BOTH, expand=True, pady=10)
        
        info_frame = Frame(info_border, bg="white")
        info_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        # Main container for content
        main_content = Frame(info_frame, bg="white")
        main_content.pack(fill=BOTH, expand=True, padx=15, pady=10)
        
        # LEFT COLUMN - Quick Actions
        left_column = Frame(main_content, bg="white")
        left_column.pack(side=LEFT, fill=Y, padx=(0, 15))
        
        lbl_actions_title = Label(left_column, text="⚡ Quick Actions", 
                                 font=("Segoe UI", 14, "bold"),
                                 bg="white", fg="#1A3E6F")
        lbl_actions_title.pack(anchor=W, pady=(0, 10))
        
        actions = [
            ("➕ Add Course", self.add_course, "#E8692A"),
            ("👨‍🎓 Register Student", self.add_student, "#2B6CB0"),
            ("📝 Enter Results", self.add_result, "#1ABC9C"),
            ("📊 View Reports", self.add_report, "#8E44AD"),
        ]
        
        for text, cmd, color in actions:
            btn = Button(left_column, text=text, font=("Segoe UI", 10, "bold"),
                        bg=color, fg="white", cursor="hand2", relief=FLAT,
                        activebackground="#1A3E6F", command=cmd,
                        width=18, pady=10)
            btn.pack(fill=X, pady=4)
        
        # RIGHT COLUMN - Multiple sections
        right_column = Frame(main_content, bg="white")
        right_column.pack(side=RIGHT, fill=BOTH, expand=True)
        
        # TOP RIGHT - Recent Activity
        activity_section = Frame(right_column, bg="#F5F5F5", relief=GROOVE, bd=1)
        activity_section.pack(fill=BOTH, expand=True, pady=(0, 8))
        
        lbl_recent = Label(activity_section, text="📋 Recent Activity", 
                          font=("Segoe UI", 12, "bold"),
                          bg="#F5F5F5", fg="#1A3E6F")
        lbl_recent.pack(anchor=W, padx=10, pady=(8, 5))
        
        self.activity_list = Listbox(activity_section, font=("Segoe UI", 9),
                                     bg="white", fg="#333", bd=0,
                                     highlightthickness=0, height=5)
        self.activity_list.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Sample activities
        sample_activities = [
            "✅ System initialized successfully",
            "📚 Ready to manage courses",
            "👨‍🎓 Ready to register students",
        ]
        for act in sample_activities:
            self.activity_list.insert(END, act)
        
        # MIDDLE RIGHT - System Status
        status_section = Frame(right_column, bg="#E8F5E9", relief=GROOVE, bd=1)
        status_section.pack(fill=BOTH, expand=True, pady=(0, 8))
        
        lbl_status = Label(status_section, text="🔧 System Status",
                          font=("Segoe UI", 12, "bold"),
                          bg="#E8F5E9", fg="#1A3E6F")
        lbl_status.pack(anchor=W, padx=10, pady=(8, 5))
        
        status_items = [
            ("Database", "✅ Connected"),
            ("Server", "✅ Running"),
            ("Backup", "✅ Updated"),
        ]
        
        for label, status in status_items:
            status_frame = Frame(status_section, bg="#E8F5E9")
            status_frame.pack(fill=X, padx=10, pady=2)
            
            lbl_label = Label(status_frame, text=label, font=("Segoe UI", 9),
                            bg="#E8F5E9", fg="#333")
            lbl_label.pack(side=LEFT)
            
            lbl_stat = Label(status_frame, text=status, font=("Segoe UI", 9, "bold"),
                           bg="#E8F5E9", fg="#2E7D32")
            lbl_stat.pack(side=RIGHT)
        
        # BOTTOM RIGHT - Quick Stats
        stats_section = Frame(right_column, bg="#E3F2FD", relief=GROOVE, bd=1)
        stats_section.pack(fill=BOTH, expand=True)
        
        lbl_stats = Label(stats_section, text="📊 Quick Stats",
                         font=("Segoe UI", 12, "bold"),
                         bg="#E3F2FD", fg="#1A3E6F")
        lbl_stats.pack(anchor=W, padx=10, pady=(8, 5))
        
        stats_data = [
            ("Pass Rate", "92.5%"),
            ("Active Users", "45"),
            ("Last Backup", "Today"),
        ]
        
        for label, value in stats_data:
            stats_frame = Frame(stats_section, bg="#E3F2FD")
            stats_frame.pack(fill=X, padx=10, pady=2)
            
            lbl_label = Label(stats_frame, text=label, font=("Segoe UI", 9),
                            bg="#E3F2FD", fg="#333")
            lbl_label.pack(side=LEFT)
            
            lbl_value = Label(stats_frame, text=value, font=("Segoe UI", 9, "bold"),
                            bg="#E3F2FD", fg="#1976D2")
            lbl_value.pack(side=RIGHT)
    
    def _create_stat_card_responsive(self, parent, icon, label, color, column):
        """Create a responsive statistics card"""
        frame = Frame(parent, bg=color, relief=FLAT)
        frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
        
        inner = Frame(frame, bg=color)
        inner.pack(fill=BOTH, expand=True, padx=15, pady=15)
        
        lbl_icon = Label(inner, text=icon, font=("Segoe UI", 32),
                         bg=color, fg="white")
        lbl_icon.pack(side=LEFT, padx=(0, 10))
        
        right_frame = Frame(inner, bg=color)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        
        lbl_value = Label(right_frame, text="0", font=("Segoe UI", 28, "bold"),
                          bg=color, fg="white", anchor="e")
        lbl_value.pack(fill=X)
        
        lbl_label = Label(right_frame, text=label, font=("Segoe UI", 12, "bold"),
                          bg=color, fg="white", anchor="e")
        lbl_label.pack(fill=X)
        
        return lbl_value
    
    def _create_footer(self):
        """Create footer"""
        footer = Frame(self.root, bg="#1A3E6F", height=35)
        footer.pack(side=BOTTOM, fill=X)
        
        lbl_footer = Label(footer, text="SRMS — Student Result Management System | A.S. College, Khanna",
                          font=("Segoe UI", 9, "bold"), bg="#1A3E6F", fg="#A8C4E0")
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