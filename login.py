from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from tkinter import ttk, messagebox
from datetime import datetime
from math import sin, cos, radians
import sqlite3
import os

class Login_window:
    def __init__(self, root):
        self.root = root
        self.root.title("SRMS — Login")
        self.root.geometry("1100x650+100+50")
        self.root.config(bg="#F0F4F8")
        self.root.resizable(False, False)

        # Main container
        main_frame = Frame(self.root, bg="#F0F4F8")
        main_frame.pack(fill=BOTH, expand=True)

        # Left Panel - Welcome & Clock
        left_panel = Frame(main_frame, bg="#1A3E6F", width=500)
        left_panel.pack(side=LEFT, fill=Y, expand=False)
        left_panel.pack_propagate(False)

        # Welcome text
        welcome_frame = Frame(left_panel, bg="#1A3E6F")
        welcome_frame.pack(pady=(50, 20))
        Label(welcome_frame, text="🎓", font=("Segoe UI", 48), bg="#1A3E6F", fg="white").pack()
        Label(welcome_frame, text="STUDENT RESULT", font=("Segoe UI", 24, "bold"), bg="#1A3E6F", fg="white").pack()
        Label(welcome_frame, text="MANAGEMENT SYSTEM", font=("Segoe UI", 20, "bold"), bg="#1A3E6F", fg="white").pack()
        Label(welcome_frame, text="A.S. College, Khanna", font=("Segoe UI", 12), bg="#1A3E6F", fg="#A8C4E0").pack(pady=(10, 0))

        # Clock
        self.clock_lbl = Label(left_panel, bg="#1A3E6F")
        self.clock_lbl.pack(pady=30)
        self.lbl_time = Label(left_panel, font=("Segoe UI", 18, "bold"), bg="#1A3E6F", fg="white")
        self.lbl_time.pack()
        self.lbl_date = Label(left_panel, font=("Segoe UI", 11), bg="#1A3E6F", fg="#A8C4E0")
        self.lbl_date.pack()

        # Right Panel - Login Form
        right_panel = Frame(main_frame, bg="white", width=600)
        right_panel.pack(side=RIGHT, fill=BOTH, expand=True)

        # Form container
        form_frame = Frame(right_panel, bg="white")
        form_frame.pack(expand=True, padx=50, pady=60)

        # Title
        Label(form_frame, text="Login to Your Account", font=("Segoe UI", 24, "bold"),
              bg="white", fg="#1A3E6F").pack(anchor="w", pady=(0, 10))
        Label(form_frame, text="Welcome back! Please enter your credentials.",
              font=("Segoe UI", 11), bg="white", fg="#7F8C8D").pack(anchor="w", pady=(0, 30))

        # Email
        Label(form_frame, text="Email Address", font=("Segoe UI", 12, "bold"),
              bg="white", fg="#333").pack(anchor="w")
        self.txt_email = Entry(form_frame, font=("Segoe UI", 12), bg="#F0F4F8",
                               relief=SOLID, bd=1, highlightthickness=1,
                               highlightcolor="#1A3E6F", highlightbackground="#DDD")
        self.txt_email.pack(fill=X, pady=(5, 20), ipady=8)

        # Password
        Label(form_frame, text="Password", font=("Segoe UI", 12, "bold"),
              bg="white", fg="#333").pack(anchor="w")
        self.txt_pass = Entry(form_frame, font=("Segoe UI", 12), bg="#F0F4F8",
                              relief=SOLID, bd=1, show="•", highlightthickness=1,
                              highlightcolor="#1A3E6F", highlightbackground="#DDD")
        self.txt_pass.pack(fill=X, pady=(5, 20), ipady=8)

        # Login Button
        btn_login = Button(form_frame, text="Login", font=("Segoe UI", 13, "bold"),
                           bg="#2B6CB0", fg="white", cursor="hand2", relief=FLAT,
                           activebackground="#1A3E6F", command=self.login, pady=8)
        btn_login.pack(fill=X, pady=(10, 15))

        # Links
        link_frame = Frame(form_frame, bg="white")
        link_frame.pack(fill=X, pady=10)

        btn_register = Button(link_frame, text="Create New Account", font=("Segoe UI", 10),
                              bd=0, cursor="hand2", fg="#2B6CB0", bg="white",
                              activebackground="white", command=self.register_window)
        btn_register.pack(side=LEFT)

        btn_forget = Button(link_frame, text="Forgot Password?", font=("Segoe UI", 10),
                            bd=0, cursor="hand2", fg="#E8692A", bg="white",
                            activebackground="white", command=self.forget_password)
        btn_forget.pack(side=RIGHT)

        # Start clock
        self.update_clock()

    def update_clock(self):
        """Update analog clock and digital time display"""
        now = datetime.now()
        h = now.hour % 12
        m = now.minute
        s = now.second

        hr_angle = (h / 12) * 360 + (m / 60) * 30
        min_angle = (m / 60) * 360
        sec_angle = (s / 60) * 360

        self.draw_clock(hr_angle, min_angle, sec_angle)

        self.lbl_time.config(text=now.strftime("%I:%M:%S %p"))
        self.lbl_date.config(text=now.strftime("%A, %d %B %Y"))

        self.root.after(1000, self.update_clock)

    def draw_clock(self, hr, min_, sec):
        """Draw analog clock on left panel"""
        size = 200
        cx = cy = size // 2
        img = Image.new("RGB", (size, size), (26, 62, 111))  # #1A3E6F approximate
        draw = ImageDraw.Draw(img)

        # Clock face
        draw.ellipse((5, 5, size-5, size-5), outline="white", width=2)
        draw.ellipse((10, 10, size-10, size-10), outline="#A8C4E0", width=1)

        # Hour markers
        for i in range(12):
            angle = radians(i * 30)
            r1, r2 = cx - 15, cx - 8
            draw.line((cx + r1 * sin(angle), cy - r1 * cos(angle),
                       cx + r2 * sin(angle), cy - r2 * cos(angle)),
                      fill="white", width=3 if i % 3 == 0 else 1)

        # Hands
        def draw_hand(angle, length, color, width):
            rad = radians(angle)
            draw.line((cx, cy, cx + length * sin(rad), cy - length * cos(rad)),
                      fill=color, width=width)

        draw_hand(hr, 60, "#E8692A", 4)
        draw_hand(min_, 85, "#1ABC9C", 3)
        draw_hand(sec, 90, "white", 2)

        # Center dot
        draw.ellipse((cx-4, cy-4, cx+4, cy+4), fill="#E8692A")

        self.clock_img = ImageTk.PhotoImage(img)
        self.clock_lbl.config(image=self.clock_img)

    def register_window(self):
        self.root.destroy()
        os.system("python register.py")

    def forget_password(self):
        self.root2 = Toplevel(self.root)
        self.root2.title("Reset Password")
        self.root2.geometry("450x550+350+150")
        self.root2.config(bg="white")
        self.root2.resizable(False, False)

        # Title
        Label(self.root2, text="Reset Password", font=("Segoe UI", 20, "bold"),
              bg="white", fg="#1A3E6F").pack(pady=(30, 10))

        # Email
        Label(self.root2, text="Email Address", font=("Segoe UI", 12, "bold"),
              bg="white", fg="#333").pack(anchor="w", padx=40, pady=(20, 5))
        self.fp_email = Entry(self.root2, font=("Segoe UI", 12), bg="#F0F4F8",
                              relief=SOLID, bd=1)
        self.fp_email.pack(fill=X, padx=40, pady=(0, 15), ipady=6)

        # Security Question
        Label(self.root2, text="Security Question", font=("Segoe UI", 12, "bold"),
              bg="white", fg="#333").pack(anchor="w", padx=40, pady=(5, 5))
        self.cmb_quest = ttk.Combobox(self.root2, font=("Segoe UI", 11), state="readonly")
        self.cmb_quest['values'] = ("Select", "Your Birth Place", "Your Girlfriend Name", "Your Pet Name")
        self.cmb_quest.pack(fill=X, padx=40, pady=(0, 15), ipady=5)
        self.cmb_quest.current(0)

        # Answer
        Label(self.root2, text="Answer", font=("Segoe UI", 12, "bold"),
              bg="white", fg="#333").pack(anchor="w", padx=40, pady=(5, 5))
        self.txt_answer = Entry(self.root2, font=("Segoe UI", 12), bg="#F0F4F8",
                                relief=SOLID, bd=1)
        self.txt_answer.pack(fill=X, padx=40, pady=(0, 15), ipady=6)

        # New Password
        Label(self.root2, text="New Password", font=("Segoe UI", 12, "bold"),
              bg="white", fg="#333").pack(anchor="w", padx=40, pady=(5, 5))
        self.txt_new_pass = Entry(self.root2, font=("Segoe UI", 12), bg="#F0F4F8",
                                  relief=SOLID, bd=1, show="•")
        self.txt_new_pass.pack(fill=X, padx=40, pady=(0, 20), ipady=6)

        # Reset Button
        btn_reset = Button(self.root2, text="Reset Password", font=("Segoe UI", 13, "bold"),
                           bg="#2B6CB0", fg="white", cursor="hand2", relief=FLAT,
                           command=self.reset_password, pady=8)
        btn_reset.pack(fill=X, padx=40, pady=(10, 20))

    def reset_password(self):
        if self.cmb_quest.get() == "Select" or self.txt_answer.get() == "" or self.txt_new_pass.get() == "" or self.fp_email.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root2)
            return
        if len(self.txt_new_pass.get()) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters", parent=self.root2)
            return

        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM employee WHERE email=? AND question=? AND answer=?",
                        (self.fp_email.get(), self.cmb_quest.get(), self.txt_answer.get()))
            row = cur.fetchone()
            if row is None:
                messagebox.showerror("Error", "Incorrect email, question or answer", parent=self.root2)
            else:
                cur.execute("UPDATE employee SET password=? WHERE email=?",
                            (self.txt_new_pass.get(), self.fp_email.get()))
                con.commit()
                messagebox.showinfo("Success", "Password reset successfully!", parent=self.root2)
                self.root2.destroy()
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root2)

    def login(self):
        if self.txt_email.get().strip() == "" or self.txt_pass.get() == "":
            messagebox.showerror("Error", "Please enter email and password", parent=self.root)
            return
        try:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM employee WHERE email=? AND password=?",
                        (self.txt_email.get().strip(), self.txt_pass.get()))
            row = cur.fetchone()
            if row is None:
                messagebox.showerror("Error", "Invalid Email or Password", parent=self.root)
            else:
                messagebox.showinfo("Success", f"Welcome {row[1]} {row[2]}!", parent=self.root)
                self.root.destroy()
                os.system("python hi.py")
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root= Tk()
    root.tk.call('tk', 'scaling', 1.4)
    obj = Login_window(root)
    root.mainloop()